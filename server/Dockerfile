FROM python:3
WORKDIR /app
ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt')"
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('bert-base-nli-mean-tokens')"
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
