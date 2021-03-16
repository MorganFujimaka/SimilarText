<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Text</h1>
        <br><br>
        <table class="table table-hover">
          <tbody>
            <tr v-for="(sent, index) in text" :key="index">
              <td>
                <router-link :to="'/sentences/' + sent.id">{{ sent.body }}</router-link>
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
      text: [],
    };
  },
  methods: {
    getText(id) {
      const path = `http://localhost:5000/texts/${id}`;
      axios.get(path)
        .then((res) => {
          this.text = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getText(this.$route.params.id);
  },
};
</script>

<style scoped>
a {
  color: #212529;
}

a:hover {
  text-decoration: none;
  color: #212529;
}
</style>
