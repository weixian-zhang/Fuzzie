<!-- https://pictogrammers.github.io/@mdi/font/6.9.96/ -->

<template>
  <v-card
  color="white"
  outlined
  width="100%"
  height="100%">
    <v-toolbar color="blue" dense flat="true" height="50px">
      <v-spacer />
      <v-btn icon height="30px" width="30px">
        <v-icon>mdi-card-plus</v-icon>
      </v-btn>
    </v-toolbar>
    <div>
      
    </div>
  </v-card>
  

</template>

<script>

import "vue3-treeview/dist/style.css";
import { Options, Vue } from 'vue-class-component';

@Options({
  components: {
    
  },
  props: {
    // msg: String
  }
})
export default class ApiDiscovery extends Vue {

  config = {
        roots: ["id1", "id2"],
      }
  fuzzcontexts =  {
        id1: {
          text: "text1",
          children: ["id11", "id12"],
        },
        id11: {
          text: "text11",
        },
        id12: {
          text: "text12",
        },
        id2: {
          text: "text2",
        }
      }

  mounted() {
    //this.getFuzzcontexts()
  }

  
  getFuzzcontexts() {
    //this.fuzzcontexts = []
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
