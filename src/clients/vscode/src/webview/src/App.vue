<template>
  <Master />
</template>

<script lang="ts">

import { Options, Vue } from 'vue-class-component';
import HelloWorld from './components/HelloWorld.vue';
import Master from './components/Master.vue'
import BootstrapVue3 from 'bootstrap-vue-3';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';

// Vue.use(BootstrapVue);

@Options({
  components: {
    HelloWorld,
    Master
  },
})
export default class App extends Vue {}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
