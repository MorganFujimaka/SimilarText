import os
import time
import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from elasticsearch import Elasticsearch
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from langdetect import detect

sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

es_host = os.getenv("ELASTICSEARCH_URL", "localhost:9200")
es = Elasticsearch([es_host])

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

with app.app_context():
    mapping_file = open(os.path.join(app.root_path, "mapping.json"), "r")
    mapping = json.load(mapping_file)

    while not es.ping():
        time.sleep(2)

    es.indices.create(index="texts", body=mapping["texts"], ignore=400)
    es.indices.create(index="sentences", body=mapping["sentences"], ignore=400)


def index_sentences(text, text_id):
    sentences = sent_tokenize(text)
    embeddings = sbert_model.encode(sentences)

    for sent, embedding in zip(sentences, embeddings):
        es.index(
            index="sentences",
            body={"text_id": text_id, "body": sent, "embedding": embedding},
            refresh="true"
        )


def search_similar_sentences(sentence_id, embedding):
    query_body = {
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                        "must_not": {
                            "term": {"_id": sentence_id}
                        }
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding')+1.0",
                    "params": {
                        "query_vector": embedding
                    }
                }
            }
        },
        "size": 100
    }

    es_response = es.search(index="sentences", body=query_body)

    similar_sentences = []
    for doc in es_response["hits"]["hits"]:
        similar_sentences.append({
            "id": doc["_id"],
            "similarity": "{:.3f}".format(doc["_score"]-1),
            "body": doc["_source"]["body"],
            "text_id": doc["_source"]["text_id"]
        })

    return similar_sentences


@app.route('/')
def api_root():
    return "Welcome to SimilarText"


@app.route('/texts', methods=['GET'])
def show_texts():
    es_response = es.search(index="texts", body={"query": {"match_all": {}}, "size": 1000})

    response = []
    for doc in es_response["hits"]["hits"]:
        response.append({"id": doc["_id"], "body": doc["_source"]["body"]})

    return jsonify(response)


@app.route('/texts', methods=['POST'])
def create_text():
    text = request.json["body"]
    text_lang = detect(text)

    if text_lang != "en":
        return jsonify({"error": "English texts only allowed"}), 400

    es_response = es.index(index="texts", body={"body": text})
    text_id = es_response["_id"]

    index_sentences(text, text_id)

    return jsonify({"id": text_id, "body": text})


@app.route('/texts/<text_id>', methods=['GET'])
def show_text(text_id):
    query_body = {
        "query": {
            "term": {
                "text_id": text_id
            }
        }
    }

    es_response = es.search(index="sentences", body=query_body)

    response = []
    for doc in es_response["hits"]["hits"]:
        response.append({"id": doc["_id"], "body": doc["_source"]["body"]})

    return jsonify(response)


@app.route('/sentences/<sentence_id>', methods=['GET'])
def show_sentence(sentence_id):
    doc = es.get(index="sentences", doc_type="_doc", id=sentence_id)

    response = {
        "id": doc["_id"],
        "body": doc["_source"]["body"],
        "similar_sentences": search_similar_sentences(sentence_id, doc["_source"]["embedding"])
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
