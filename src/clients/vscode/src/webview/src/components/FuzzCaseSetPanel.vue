
<!-- https://primefaces.org/primevue/treetable/responsive -->

<template>

  <v-card
  color="white"
  outlined
  width="100%"
  height="100%">
    <v-toolbar card color="cyan" flat dense height="50px">
      <v-spacer />
      <!-- <v-btn icon height="30px" width="30px">
        <v-icon :disabled="!isFuzzcontextsGetComplete" @click="getFuzzcontexts">mdi-refresh</v-icon>
      </v-btn> -->
      <v-btn icon height="30px" width="30px">
        <v-icon >mdi-card-plus</v-icon>
      </v-btn>
    </v-toolbar>

      <v-table density="compact" fixed-header>
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
            v-for="item in fuzzcasesetRunSummary"
            :key="item.fuzzCaseSetId">
            <td>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" v-model="item.selected">
              </div>

            </td>
            <td>{{ item.verb }}</td>
            <td>{{ item.path }}</td>
            <td>{{ shortenBody(item.body, 20) }}</td>

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

import { Options, Vue } from 'vue-class-component';
import DataTable from 'primevue/datatable';

@Options({
  components: {
    DataTable
  },
  props: {
    // msg: String
  }
})

 export default class FuzzCaseSetPanel extends Vue {


  // fuzzCaseSetId
  //   fuzzCaseSetRunId
  //   fuzzcontextId
  //   selected
  //   verb
  //   path
  //   querystringNonTemplate
  //   bodyNonTemplate
  //   headerNonTemplate
  //   authnType
  //   runSummaryId
  //   http2xx
  //   http3xx
  //   http4xx
  //   http5xx
  //   completedDataCaseRuns 

 fuzzcasesetRunSummary = [
          {
            
            fuzzCaseSetId: "ASDASAsas",
            fuzzCaseSetRunId: "ASDASAsas",
            fuzzcontextId: "ASDASAsas",
            selected: true,
            verb: 'GET',
            path: '/when/{id}?name={name}',
            body: '{"a":"b","a":"b","a":"b","a":"b","a":"b","a":"b","a":"b"}',
            runSummaryId: "asdasada",
            http2xx: 0,
            http3xx: 0,
            http4xx: 0,
            http5xx: 0,
            completedDataCaseRuns : 0,
            data: {}
          },
          
        ]

  selectAll = true;

  showTable = true; //this.nodes.length > 0 ? "true": "false";

  selectAllChanged(event) {
    this.fuzzcasesetRunSummary.forEach(fcs => {
      fcs.selected = this.selectAll;
    });
  }

  shortenBody(bodyJson, length)
  {
    return bodyJson.substring(0, length) + "..."
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
 