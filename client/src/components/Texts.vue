<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Texts</h1>
        <br>
        <alert :message="message" :variant="alertVariant" v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.text-modal>Add Text</button>
        <br><br>
        <table class="table table-hover">
          <tbody>
            <tr v-for="(text, index) in texts" :key="index">
              <td>{{ index + 1 }}</td>
              <td>
                <router-link :to="'/texts/' + text.id">{{ text.body }}</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <b-modal ref="addTextModal"
             id="text-modal"
             title="Add a new text"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group">
          <b-form-textarea id="form-title-textarea"
                        type="text"
                        rows=10
                        v-model="addTextForm.body"
                        required
                        placeholder="Enter text">
          </b-form-textarea>
        </b-form-group>
        <b-button type="submit" variant="primary" class="mr-1">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      texts: [],
      addTextForm: {
        body: '',
      },
      message: '',
      showMessage: false,
      alertVariant: '',
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getTexts() {
      const path = 'http://localhost:5000/texts';
      axios.get(path)
        .then((res) => {
          this.texts = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addText(payload) {
      const path = 'http://localhost:5000/texts';
      axios.post(path, payload)
        .then((response) => {
          this.$router.push({ path: `/texts/${response.data.id}` });
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.message = error.response.data.error;
          this.alertVariant = 'danger';
          this.delayedAlert();
          this.getTexts();
        });
    },
    initForm() {
      this.addTextForm.body = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addTextModal.hide();
      const payload = { body: this.addTextForm.body };
      this.addText(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addTextModal.hide();
      this.initForm();
    },
    delayedAlert() {
      this.showMessage = true;
      setTimeout(() => {
        this.showMessage = false;
        this.message = '';
      }, 3000);
    },
  },
  created() {
    this.getTexts();
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
