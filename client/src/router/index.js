import Vue from 'vue';
import VueRouter from 'vue-router';
import Texts from '../components/Texts.vue';
import Text from '../components/Text.vue';
import Sentence from '../components/Sentence.vue';
import 'bootstrap/dist/css/bootstrap.css';

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      alias: '/texts',
      name: 'Texts',
      component: Texts,
    },
    {
      path: '/texts/:id',
      name: 'Text',
      component: Text,
      props: true,
    },
    {
      path: '/sentences/:id',
      name: 'Sentence',
      component: Sentence,
      props: true,
    },
  ],
});

export default router;
