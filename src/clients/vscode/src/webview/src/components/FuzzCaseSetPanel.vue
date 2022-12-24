
<!-- https://primefaces.org/primevue/treetable/responsive -->

<template>
  <v-card
    color="white"
    outlined
    style="display: flex; flex-flow: column; height: 100%;">
  
  <Sidebar v-model:visible="showFullValueSideBar" position="right" style="width:500px;">
    <v-textarea auto-grow
          outlined
          rows="1"
          readonly
          v-model="tableValViewInSizeBar" />
  </Sidebar>

    <v-toolbar card color="#F6F6F6" flat density="compact" dense height="50px">
      <v-toolbar-title>Fuzz Cases</v-toolbar-title>
      
      
        <v-btn v-tooltip.bottom="'save'" icon  variant="plain" height="30px" plain 
          :disabled="saveBtnDisabled"
          @click="(
            saveFuzzCaseSets
            )">
          <v-badge  color="pink" dot v-model="isTableDirty">
            <v-icon color="cyan darken-3">mdi-content-save-settings-outline</v-icon>
          </v-badge>
        </v-btn>
    </v-toolbar>
      
      <v-table density="compact" fixed-header height="350px" hover="true" >
        <thead>
          <tr>
            <th class="text-left">
              <div class="form-check">
                <v-checkbox color="cyan" id="flexCheckDefault" label="All" v-model="selectAll" density="compact" @change="(
                  selectAllChanged($event))"  hide-details />
                <!-- <input class="form-check-input" type="checkbox" id="flexCheckDefault" v-model="selectAll" 
                @change="(
                  selectAllChanged($event))">
                <label class="form-check-label" for="flexCheckDefault">
                  All
                </label> -->
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
              File Type
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
            @click="onRowClick(item), selectedRow= item.fuzzCaseSetId"
            :style="item.fuzzCaseSetId === selectedRow ? 'background-color:lightgrey;' : ''">

            <td>
              <div class="form-check">
                <v-checkbox color="cyan" id="flexCheckDefault" label="" v-model="item.selected"  density="compact" @click="isTableDirty=true"  hide-details />

                <!-- <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" v-model="item.selected" 
                @click="isTableDirty=true"> -->
              </div>

            </td>
            <td>{{ item.verb }}</td>
            
            <td>
              <span style="cursor: pointer" @click="(
                onTableValueNonJsonSeeInFullClicked(item.path),
                showFullValueSideBar = true
              )">
                {{ shortenJsonValueInTable(item.path) }}
              </span>
            </td>
            
            <td>
              <span style="cursor: pointer" @click="(
                onTableValueSeeInFullClicked(item.headerNonTemplate),
                showFullValueSideBar = true
              )">
                {{ shortenJsonValueInTable(item.headerNonTemplate, 40) }} 
              </span>
            </td>
            <td>
              <span style="cursor: pointer" @click="(
                onTableValueSeeInFullClicked(item.bodyNonTemplate),
                showFullValueSideBar = true
              )"> 
              {{ shortenJsonValueInTable(item.bodyNonTemplate, 40) }} 
              </span>
            </td>
            <td>
              {{ item.file }}
            </td>
            <td>
              {{ item.http2xx == undefined ? 0 : item.http2xx }}
            </td>
            <td>
              {{ item.http3xx == undefined ? 0 : item.http3xx }}
            </td>
            <td>
              {{ item.http4xx == undefined ? 0 : item.http4xx }}
            </td>
            <td>
              {{ item.http5xx == undefined ? 0 : item.http5xx }}
            </td>
            <td>
              {{ item.completedDataCaseRuns == undefined ? 0 : item.completedDataCaseRuns  }} / {{ item.totalDataCaseRunsToComplete }}
            </td>
            
          </tr>
        </tbody>
      </v-table>

  </v-card>

</template>
      

<script lang="ts">

import { inject } from 'vue';
import Logger from '../Logger';
import { Options, Vue  } from 'vue-class-component';
// import { Watch } from 'vue-property-decorator'
import DataTable from 'primevue/datatable';
import Sidebar from 'primevue/sidebar';
import Utils from '../Utils';
import { ApiFuzzCaseSetsWithRunSummaries } from '../Model';
import FuzzerWebClient from "../services/FuzzerWebClient";
import FuzzerManager from "../services/FuzzerManager";

class Props {
  toastInfo: any = {};
  toastError: any = {};
  toastSuccess: any = {};
  eventemitter: any = {}
  fuzzermanager: FuzzerManager
  webclient : FuzzerWebClient
}

@Options({
  components: {
    DataTable,
    Sidebar
  },
  watch: {

  }
})

 export default class FuzzCaseSetPanel extends Vue.with(Props) {

  fcsRunSums: Array<ApiFuzzCaseSetsWithRunSummaries| any> = [];

  //fuzzingfcsRunSums: Array<ApiFuzzCaseSetsWithRunSummaries> = [];

  //dataCache = {};

  $logger: Logger|any;

  selectedRow = '';

  selectAll = true;

  showTable = true;

  saveBtnDisabled = false;

  showFullValueSideBar = false;

  isTableDirty = false;

  tableValViewInSizeBar = '';

  fuzzerConnected = false;

  currentFuzzContextId = '';

  fuzzContextId = '';
  fuzzCaseSetRunsId = '';

  beforeMount() {
      this.$logger = inject('$logger');   
  }

  onTableValueSeeInFullClicked(jsonValue) {
      this.tableValViewInSizeBar = JSON.stringify(JSON.parse(jsonValue),null,'\t')
  }

  onTableValueNonJsonSeeInFullClicked(val) {
    this.tableValViewInSizeBar = val
  }

  mounted(){
    //event from master
    this.eventemitter.on('fuzzer.ready', this.onFuzzStartReady);
    this.eventemitter.on('fuzzer.notready', this.onFuzzerNotReady);

    // listen to ApiDiscovery Tree item select event
    this.eventemitter.on("onFuzzContextSelected", this.onFuzzContextSelected);
    this.eventemitter.on("onFuzzCaseSetRunSelected", this.onFuzzCaseSetRunSelected);
    
    this.eventemitter.on("onFuzzContextDelete", this.onFuzzContextDeleted);
    this.eventemitter.on("onFuzzContextRefreshClicked", this.onFuzzContextRefreshClicked);
    
    //websocket events from fuzzer
    this.eventemitter.on('fuzz.update.casesetrunsummary', this.onFuzzingUpdateRunSummary);

    this.eventemitter.on('fuzzer.notready', this.onFuzzerNotReady);

  }

  // #### websocket events ####

  onFuzzStartReady() {
    this.fuzzerConnected = true;
  }

  onFuzzerNotReady() {
    this.clearData()
    this.fuzzerConnected = false;

    this.currentFuzzContextId = '';
  }

 
  onFuzzingUpdateRunSummary(runSummary: ApiFuzzCaseSetsWithRunSummaries) {

    this.fcsRunSums.map(x => {
      if(x.fuzzCaseSetId == runSummary.fuzzCaseSetId && runSummary.fuzzCaseSetRunId == this.fuzzCaseSetRunsId) {
        x.http2xx = runSummary.http2xx;
        x.http3xx = runSummary.http3xx;
        x.http4xx = runSummary.http4xx;
        x.http5xx = runSummary.http5xx;
        x.completedDataCaseRuns = runSummary.completedDataCaseRuns;

        return;
      }
    });
  }


  async saveFuzzCaseSets() {

    if(!this.isTableDirty) {
      this.toastInfo('no changes to save');
      return;
    }
    

    this.saveBtnDisabled = true;

    const newFCS = this.fcsRunSums.map(x => {
      return {
        fuzzCaseSetId: x.fuzzCaseSetId,
        selected: x.selected
      }
    });

    const [ok, error] = await this.fuzzermanager.saveFuzzCaseSetSelected(newFCS);

    if(!ok)
      {
        this.toastError(error, 'Update Fuzz Cases');
      }
      else
      {
        this.isTableDirty = false;
        this.toastSuccess('Fuzz Cases are updated successfully', 'Update Fuzz Cases');
      }

    this.saveBtnDisabled = false;
  }

  onFuzzContextDeleted(fuzzcontextId) {

    this.clearData();
  }

  onFuzzContextRefreshClicked() {
    this.clearData();
  }

  public async getFuzzCaseSet_And_RunSummaries(fuzzcontextId: string, fuzzCaseSetRunsId: string)
  {
     const [ok, error, result] = await this.fuzzermanager.getApiFuzzCaseSetsWithRunSummaries(fuzzcontextId, fuzzCaseSetRunsId);

    if(!ok)
    {
      this.toastError(error, 'Get Fuzz Cases');
    }
    else
    {
      if(!Utils.isNothing(result)){
        this.fcsRunSums = result;
      }
      
    }
  }

  async onFuzzContextSelected(fuzzcontextId)
  {
     this.fuzzContextId = fuzzcontextId;
     await this.getFuzzCaseSet_And_RunSummaries(fuzzcontextId, '');
  }

  async onFuzzCaseSetRunSelected(fuzzcontextId: string, fuzzCaseSetRunsId: string)
  {
    this.fuzzContextId = fuzzcontextId;
    this.fuzzCaseSetRunsId = fuzzCaseSetRunsId;
     await this.getFuzzCaseSet_And_RunSummaries(fuzzcontextId, fuzzCaseSetRunsId);
  }
  

  onRowClick(fcsrs: ApiFuzzCaseSetsWithRunSummaries) {
    // send event to FuzzResult panel to display request and response
    this.eventemitter.emit("onFuzzCaseSetSelected", fcsrs.fuzzCaseSetId, fcsrs.fuzzCaseSetRunId);
  }

  selectAllChanged(event) {
    this.fcsRunSums.forEach((fcs: ApiFuzzCaseSetsWithRunSummaries) => {
      fcs.selected = this.selectAll;
    });
    this.isTableDirty = true;
  }

  shortenJsonValueInTable(bodyJson, length=40)
  {
    return Utils.shortenStr(bodyJson, length);
  }

  clearData() {
      this.fcsRunSums = [];
      //this.dataCache = {};
      this.selectedRow = ''
  }

 }
 
 </script>
 
 <!-- Add "scoped" attribute to limit CSS to this component only -->
 <style scoped>

.custom-highlight-row{
   background-color: pink
}

.v-card {
  display: flex !important;
  flex-direction: column;
}

.v-card__text {
  flex-grow: 1;
  overflow: auto;
}

code {
  font-family: Consolas,"courier new";
  color: crimson;
  background-color: #f1f1f1;
  padding: 2px;
  font-size: 105%;
}
 </style>
 