<template>
  <div id="app">
    <router-view></router-view>
    <!-- <test-page></test-page> -->
  </div>
</template>

<script>
// import testPage from './components/testPage.vue'

export default {
  // components: { testPage },
  name:'app',
}
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
}
</style>
