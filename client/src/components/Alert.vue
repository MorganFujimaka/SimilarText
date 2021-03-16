<template>
  <div>
    <b-alert :variant="variant" show fade>{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
  props: ['variant', 'message'],
};
</script>
