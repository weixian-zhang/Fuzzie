
<!-- https://primefaces.org/primevue/treetable/responsive -->

<template>

  <v-card
  color="white"
  outlined
  height="455px"
 >
    <v-toolbar card color="cyan" flat dense height="50px">
      <v-spacer />
      
      <v-btn v-tooltip.bottom="'save'" icon  variant="plain" height="30px" plain >
        <v-icon>mdi-content-save-settings-outline</v-icon>
      </v-btn>
      <v-btn v-tooltip.left="'start fuzzing'" icon  variant="plain" height="30px" plain >
        <v-icon>mdi-lightning-bolt</v-icon>
      </v-btn>
    </v-toolbar>

      <v-table density="compact" fixed-header height="455px">
        <thead>
          <tr>
            <th class="text-left">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" id="flexCheckDefault" v-model="selectAll" @change="selectAllChanged($event)">
                <label class="form-check-label" for="flexCheckDefault">
                  Select All
                </label>
              </div>
            </th>
            <th class="text-left">
              Verb
            </th>
            <th class="text-left">
              Path
            </th>
            <th class="text-left">
              Header
            </th>
            <th class="text-left">
              Body
            </th>
            <th class="text-left">
              2xx
            </th>
            <th class="text-left">
              3xx
            </th>
            <th class="text-left">
              4xx
            </th>
            <th class="text-left">
              5xx
            </th>
            <th class="text-left">
              Total Runs
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in fcsRunSums"
            :key="item.fuzzCaseSetId"
            @click="onRowClick(item)">
            <td>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" v-model="item.selected">
              </div>

            </td>
            <td>{{ item.verb }}</td>
            <td>{{ item.path }}</td>
            <td>{{ item.header }}</td>
            <td><a href="#"> {{ shortenBody(item.body, 20) }} </a></td>

            <td>
              {{ item.http2xx }}
            </td>
            <td>
              {{ item.http3xx }}
            </td>
            <td>
              {{ item.http4xx }}
            </td>
            <td>
              {{ item.http5xx }}
            </td>
            <td>
              {{ item.completedDataCaseRuns }}
            </td>
            
          </tr>
        </tbody>
      </v-table>
  
  </v-card>
  
</template>
      
 
    
<script>

import { Options, Vue  } from 'vue-class-component';
import DataTable from 'primevue/datatable';
import FuzzerWebClient from '@/services/FuzzerWebClient';


class Props {
  // optional prop
  eventemitter = {}
}


@Options({
  components: {
    DataTable
  }
})

 export default class FuzzCaseSetPanel extends Vue.with(Props) {


  fuzzerWC = {};

  fcsRunSums = [];

  dataCache = {};

  selectAll = true;

  showTable = true; //this.nodes.length > 0 ? "true": "false";

  
  mounted(){
    this.fuzzerWC = new FuzzerWebClient();

    // listen to ApiDiscovery Tree item select event
    this.eventemitter.on("onFuzzContextSelected", this.onFuzzContextSelected)
  }

  async onFuzzContextSelected(fuzzcontextId)
  {
    if(this.dataCache[fuzzcontextId] !== undefined)
    {
      this.fcsRunSums = this.dataCache[fuzzcontextId];
    }
    else
    {
      const result = await this.fuzzerWC.getFuzzCaseSetWithRunSummary(fuzzcontextId);
      this.dataCache[fuzzcontextId] = result;
      this.fcsRunSums = this.dataCache[fuzzcontextId];
    }
  }

  onRowClick(fcsrs) {
    return;
  }

  selectAllChanged(event) {
    this.fcsRunSums.forEach(fcs => {
      fcs.selected = this.selectAll;
    });
  }

  shortenBody(bodyJson, length)
  {
    if(bodyJson != undefined && bodyJson.length > length)
    {
      return bodyJson.substring(0, length) + "...";
    }
    else
    {
      return bodyJson;
    }
  }

 }
 
 </script>
 
 <!-- Add "scoped" attribute to limit CSS to this component only -->
 <style scoped>

.v-card {
  display: flex !important;
  flex-direction: column;
}

.v-card__text {
  flex-grow: 1;
  overflow: auto;
}

 </style>
 