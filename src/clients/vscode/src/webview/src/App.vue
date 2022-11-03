<template>
  <v-app>
    <v-main>
      <Master />   
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Master from './components/Master.vue'

export default defineComponent({
  name: 'App',

  components: {
    Master
  },


  data () {
    return {
  

    }
  },
})
</script>

<style>
html,body{
    height:100%;
}

.flex-fill {
    flex:1;
}

#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50; */
  width: 100%;
  height: 100vh;
  margin-top: 5px;
}

html {
  overflow: hidden !important;
}


</style>
