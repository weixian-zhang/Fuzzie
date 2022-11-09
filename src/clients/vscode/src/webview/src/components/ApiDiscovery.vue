<!-- https://pictogrammers.github.io/@mdi/font/6.9.96/ -->

<template>
  <v-card
  color="white"
  outlined
  width="100%"
  height="100%">
    <v-toolbar card color="cyan" flat dense height="50px">
      <v-spacer />
      <v-btn icon height="30px" width="30px">
        <v-icon :disabled="!isFuzzcontextsGetComplete" @click="getFuzzcontexts">mdi-refresh</v-icon>
      </v-btn>
      <v-btn icon height="30px" width="30px">
        <v-icon >mdi-card-plus</v-icon>
      </v-btn>
    </v-toolbar>
    <div v-show="showTree">
        <Tree :value="nodes" selectionMode="single">
            <template #default="slotProps">
              <div v-on:click="onFuzzContextSelected(slotProps.node.key)">
                <b>{{slotProps.node.label}}</b>
              </div>
            </template>
            <template #url="slotProps">
                <a :href="slotProps.node.data">{{slotProps.node.label}}</a>
            </template>
        </Tree>
      </div>
  </v-card>
  
</template>

<script>

import { Options, Vue } from 'vue-class-component';
import FuzzerManager from '@/services/FuzzerManager';
import Tree from 'primevue/tree';
import dateformat from 'dateformat';
import {EventEmitter} from 'eventemitter3';

class Props {
  // optional prop
  eventemitter = {}
}

@Options({
  components: {
    Tree
  }
})
export default class ApiDiscovery extends Vue.with(Props) {

  _eventemitter = new EventEmitter();

  fm = new FuzzerManager();
  
  isFuzzcontextsGetComplete = true;

  nodes = [];

  showTree = this.nodes.length > 0 ? "true": "false";
  
  mounted() {
    this.getFuzzcontexts()
  }
  
  async getFuzzcontexts() {

    try {
      this.isFuzzcontextsGetComplete = false;
      const fcs = await this.fm.getFuzzcontexts()    

      if (fcs.length > 0)
      {
        this.nodes = this.createTreeNodesFromFuzzcontexts(fcs);
      }

      this.isFuzzcontextsGetComplete = true;
    } catch (error) {
        //TODO: log
        console.log(error)
    }
  }

  createTreeNodesFromFuzzcontexts(fcs) {

    const nodes = [];

    fcs.forEach(fc => {

        const fcNode = {
          key: fc.Id,
          label: fc.name,
          data: fc
        };

        nodes.push(fcNode)

        fc.fuzzCaseSetRuns.forEach(fcsr => {

          const casesetNode = {
            key: fcsr.fuzzCaseSetRunsId,
            label: dateformat(fcsr.startTime, "ddd, mmm dS, yyyy, h:MM:ss TT"), //`${nodeLabel.toLocaleDateString('en-us')} ${nodeLabel.toLocaleTimeString()}`,
            data: fcsr
          };
          
          if(fcNode.children == undefined)
          {
            fcNode.children = [];
          }

          fcNode.children.push(casesetNode);
        });
    });

    return nodes;

  }

  onFuzzContextSelected(fuzzContextId) {
    this.eventemitter.emit("onFuzzContextSelected", fuzzContextId);
  }

}
</script>


<style scoped>

</style>
