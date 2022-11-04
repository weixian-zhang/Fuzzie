<!-- https://pictogrammers.github.io/@mdi/font/6.9.96/ -->

<template>
  <v-card
  color="white"
  outlined
  width="100%"
  height="100%">
    <v-toolbar color="blue" flat="true" dense height="50px">
      <v-spacer />
      <v-btn icon height="30px" width="30px">
        <v-icon :disabled="!isFuzzcontextsGetComplete" @click="getFuzzcontexts">mdi-refresh</v-icon>
      </v-btn>
      <v-btn icon height="30px" width="30px">
        <v-icon >mdi-card-plus</v-icon>
      </v-btn>
    </v-toolbar>
    <div>
      
    </div>
  </v-card>
  

</template>

<script>

import { Options, Vue } from 'vue-class-component';
import FuzzerManager from '@/services/FuzzerManager';

@Options({
  components: {
    
  },
  props: {
    // msg: String
  }
})
export default class ApiDiscovery extends Vue {

  fm = new FuzzerManager();

  isFuzzcontextsGetComplete = true;
  fuzzcontexts =  [{}]

  mounted() {
    this.getFuzzcontexts()
  }

  
  async getFuzzcontexts() {
    this.isFuzzcontextsGetComplete = false;
    const fcs = await this.fm.getFuzzcontexts()
    this.isFuzzcontextsGetComplete = true;
  }
}
</script>


<style scoped>

</style>
