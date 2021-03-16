<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Sentence</h1>
        {{ sentence.body }}
        <br><br>
        <br><br>
        <h5>Similar sentences</h5>
        <table class="table table-hover">
          <tbody>
            <tr v-for="(sent, index) in sentence.similar_sentences" :key="index">
              <td>{{ sent.body }}</td>
              <td>{{ sent.similarity }}</td>
              <td style="width: 10%">
                <router-link :to="'/texts/' + sent.text_id">
                  Full text
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      sentence: {},
    };
  },
  methods: {
    getSentence(id) {
      const path = `http://localhost:5000/sentences/${id}`;
      axios.get(path)
        .then((res) => {
          this.sentence = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getSentence(this.$route.params.id);
  },
};
</script>
