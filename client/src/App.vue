<template>
  <div id="app">
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <router-link to="/">Home</router-link>
        </div>
        <br><br>
      </div>
    </div>

    <router-view/>
  </div>
</template>

<style>
#app {
  margin-top: 60px
}
</style>
