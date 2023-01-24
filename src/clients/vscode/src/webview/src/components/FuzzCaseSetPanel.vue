
<!-- https://primefaces.org/primevue/treetable/responsive -->

<template>
  <v-card
    color="white"
    outlined
    style="display: flex; flex-flow: column; height: 100%;">
  
  <Dialog v-model:visible="showReqMsgEditDialog" 
      header="Request Message Editor" 
      :breakpoints="{ '960px': '75vw', '640px': '90vw' }" :style="{ width: '80vw' }"
      :maximizable="true" :modal="true"
      :dismissableMask="false" :closeOnEscape="false"
      @hide="onDialogClose(rqInEdit)">

      <div class="container-fluid">
        <div class="row">
          <div class="col text-left">
              <RequestMessageExampleView 
              v-bind:rqmsg:loadexample="rqInEdit"
              v-on:rqmsg:loadexample="rqInEdit = $event" />
          </div>
          <div class="col text-right">
              <v-btn
                size="x-small"
                color="cyan"
                @click="parseRequestMessage(rqInEdit)"
                >
              Parse
              </v-btn>
              <v-icon v-tooltip.right="'syntax is valid'" aria-hidden="false" color="green darken-2" v-show="(!requestMsgHasError)">
                    mdi-check-circle
              </v-icon>
              <v-icon  aria-hidden="false" color="red darken-2" v-show="requestMsgHasError" v-tooltip.right="'request message has error'">
                mdi-close-circle
              </v-icon>
          </div>
        </div>
      </div>


      <div style="height: 10px;"></div>

      <codemirror
          v-model="rqInEdit"
          placeholder="request message goes here..."
          :style="{ height: '600px' }"
          :autofocus="true"
          :indent-with-tab="true"
          :tab-size="2"
          :extensions="extensions"
          @ready="onCMReady" 
        />
    </Dialog>

  <Sidebar v-model:visible="showFullValueSideBar" position="right" style="width:500px;" :modal="true" :dismissable="true">
    <v-textarea auto-grow
          outlined
          rows="1"
          readonly
          v-model="tableValViewInSizeBar" />
  </Sidebar>

    <v-toolbar card color="#F6F6F6" flat density="compact" dense height="50px">
      <v-toolbar-title>API to Fuzz</v-toolbar-title>
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
    <input class="form-control input-sm" type="text" style="height:27px;" v-model="hostnameDisplay" readonly>
      <v-table density="compact" fixed-header height="350px" hover="true" >
        <thead>
          <tr>
            <th class="text-left">
              <div class="form-check">
                <v-checkbox color="cyan" id="flexCheckDefault" label="Fuzz All" v-model="selectAll" density="compact" @change="(
                  selectAllChanged($event))"  hide-details />
              </div>
            </th>
            <th class="text-left">
            </th>
            <th class="text-left">
              Fuzz Once
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
          <tr v-show="isDataLoadingInProgress">
              <th colspan="10">
              <v-progress-linear
                    indeterminate
                    rounded
                    color="cyan">
                  </v-progress-linear>
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
              </div>
            </td>
            
            <td>
              <v-btn
                  class="ma-2"
                  variant="text"
                  icon="mdi-pencil"
                  color="cyan darken-3"
                  size="small"
                  :disabled="(isFuzzingInProgress())"
                  @click="(
                    showReqMsgEditDialog = true,
                    rqInEdit = item.requestMessage,
                    rqInEditOriginal = item.requestMessage,
                    currentEditFuzzCaseSetId = item.fuzzCaseSetId
                  )" ></v-btn>

            </td>

            <td>
                <v-btn
                  class="ma-2"
                  variant="text"
                  icon="mdi-lightning-bolt"
                  color="cyan darken-3"
                  size="small"
                  :disabled="(isFuzzingInProgress())"
                  @click="(
                        onFuzzOnce(this.selectedFuzzContextId, item.fuzzCaseSetId)
                      )" ></v-btn>
             
            </td>

            <td>{{ item.verb }}</td>
            
            <td>
              <span style="cursor: pointer"
                v-tooltip.bottom="formatLongValueForTooltip(item.path + item.querystringNonTemplate)"
                @click="(
                onTableValueNonJsonSeeInFullClicked(item.path + item.querystringNonTemplate),
                showFullValueSideBar = true
              )">
                {{ shortenValueInTable(item.path + item.querystringNonTemplate) }}
              </span>
            </td>
            
            <td>
              <span style="cursor: pointer"
               v-tooltip.bottom="formatLongValueForTooltip(item.headerNonTemplate)"
                @click="(
                onTableValueSeeInFullClicked(item.headerNonTemplate),
                showFullValueSideBar = true
              )">
                {{ shortenValueInTable(item.headerNonTemplate, 40) }} 
              </span>
            </td>
            <td>
              <span style="cursor: pointer" 
                v-tooltip.bottom="formatLongValueForTooltip(item.bodyNonTemplate)"
                @click="(
                onTableValueSeeInFullClicked(item.bodyNonTemplate),
                showFullValueSideBar = true
              )"> 
              {{ shortenValueInTable(item.bodyNonTemplate, 40) }} 
              </span>
            </td>
            <td>
              {{ item.file }}
            </td>
            <td>
              <span :class="item.http2xx > 0 ? 'font-weight-bold': ''">
                {{ item.http2xx == undefined ? 0 : (item.http2xx) }}
              </span>
            </td>
            <td>
              <span :class="item.http3xx > 0 ? 'font-weight-bold': ''">
                {{ item.http3xx == undefined ? 0 : item.http3xx }}
              </span>
            </td>
            <td>
              <span :class="item.http4xx > 0 ? 'font-weight-bold': ''">
                {{ item.http4xx == undefined ? 0 : item.http4xx }}
              </span>
            </td>
            <td>
              <span :class="item.http4xx > 0 ? 'font-weight-bold': ''">
                {{ item.http5xx == undefined ? 0 : item.http5xx }}
              </span>
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
import Dialog from 'primevue/dialog';
import DataTable from 'primevue/datatable';
import Sidebar from 'primevue/sidebar';
import Utils from '../Utils';
import { ApiFuzzCaseSetsWithRunSummaries } from '../Model';
import FuzzerWebClient from "../services/FuzzerWebClient";
import FuzzerManager from "../services/FuzzerManager";
import InputText from 'primevue/inputtext';
import RequestMessageExampleView from './RequestMessageExampleView.vue';

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
    Sidebar,
    InputText,
    Dialog,
    RequestMessageExampleView
  },
  watch: {

  }
})

 export default class FuzzCaseSetPanel extends Vue.with(Props) {

  fcsRunSums: Array<ApiFuzzCaseSetsWithRunSummaries| any> = [];

  showReqMsgEditDialog = false;
  rqInEdit = '';
  rqInEditOriginal = '';
  currentEditFuzzCaseSetId = '';

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

  hostname = '';
  port = -1;
  hostnameDisplay = ''

  rowClickEnabled = true;

  isDataLoadingInProgress = false;

  requestMsgHasError = false;
  requestMsgErrorMessage = ''

  fuzzOnceDisabled = true;

  pollFuzzResultHandler: any = undefined;
  currentFuzzingContextId = '';
  currentFuzzingCaseSetRunId = '';
  selectedFuzzContextId = '';
  selectedFuzzCaseSetId = '';
  selectedFuzzCaseSetRunId = '';

  beforeMount() {
      this.$logger = inject('$logger');   
  }

  onTableValueSeeInFullClicked(jsonValue) {
    try {
      // wordlist-type-expression could likely break json format especially {{ "custom input | my" }}
      this.tableValViewInSizeBar = JSON.stringify(JSON.parse(jsonValue),null,'\t')
    } catch (error) {
        this.tableValViewInSizeBar = jsonValue;
    }
  }

  formatLongValueForTooltip(value) {
    try {
      // wordlist-type-expression could likely break json format especially {{ "custom input | my" }}
      return JSON.stringify(JSON.parse(value),null,'\t')
    } catch (error) {
        return value;
    }
  }

  onTableValueNonJsonSeeInFullClicked(val) {
    this.tableValViewInSizeBar = val
  }

  refreshHostnameDisplay() {

    this.hostnameDisplay = '';

    if (this.hostname != '' && this.port != undefined) {
      if (this.port != 80 && this.port != 443) {
        this.hostnameDisplay = `${this.hostname}:${this.port}`;
      }
      else {
        this.hostnameDisplay = `${this.hostname}`;
      }
    }
  }

  mounted(){
    //event from master
    this.eventemitter.on('fuzz.start', this.onFuzzStart);
    this.eventemitter.on('fuzz.stop', this.onFuzzStop);
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

  async onFuzzStart(data) {

    const fuzzContextId = data.fuzzContextId;
    const fuzzCaseSetRunId = data.fuzzCaseSetRunId;

    if(this.currentFuzzingContextId != '' && this.currentFuzzingCaseSetRunId != ''){
      return;
    }

    this.currentFuzzingContextId = fuzzContextId;
    this.currentFuzzingCaseSetRunId = fuzzCaseSetRunId;

    this.intervalGetReqRespDataOnFuzz();
  }

  onFuzzStop() {

    if(!this.isFuzzingInProgress()) {
      return;
    }

    this.clearIntervalGetReqRespData();

    this.getFuzzCaseSet_And_RunSummaries(this.currentFuzzingContextId, this.currentFuzzingCaseSetRunId);

    this.currentFuzzingContextId = '';
    this.currentFuzzingCaseSetRunId = ''
  }

  onFuzzStartReady() {
    this.fuzzerConnected = true;
  }

  onFuzzerNotReady() {
    this.clearData()
    this.fuzzerConnected = false;

    this.currentFuzzContextId = '';
  }

  intervalGetReqRespDataOnFuzz() {
    if(this.isFuzzingInProgress() && this.pollFuzzResultHandler == undefined && this.currentFuzzingContextId == this.selectedFuzzContextId) {
        this.pollFuzzResultHandler = setInterval( async()=> {
              if(this.selectedFuzzContextId == this.currentFuzzingContextId ) {
                this.eventemitter.emit("onFuzzCaseSetSelected", this.selectedFuzzCaseSetId, this.currentFuzzingCaseSetRunId);
              }
              else{
                this.clearIntervalGetReqRespData();
              }
              
          },1500)
    }
  }

  clearIntervalGetReqRespData() {
    if(this.pollFuzzResultHandler != undefined) {
      clearInterval(this.pollFuzzResultHandler);
      this.pollFuzzResultHandler = undefined;
    }
  }

  // events from websocket
  onFuzzingUpdateRunSummary(runSummary: ApiFuzzCaseSetsWithRunSummaries) {

    this.fcsRunSums.map(x => {
      if(x.fuzzCaseSetId == runSummary.fuzzCaseSetId && x.fuzzCaseSetRunId == runSummary.fuzzCaseSetRunId) {
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

    if(!this.isTableDirty || this.fcsRunSums == undefined || this.fcsRunSums.length == 0) {
      this.toastInfo('no changes to save');
      return;
    }
    
    try {
      this.saveBtnDisabled = true;

      const updatedFCSList = this.fcsRunSums.map(x => {
        return {
          fuzzcontextId: x.fuzzcontextId,
          fuzzCaseSetId: x.fuzzCaseSetId,
          selected: x.selected,
          requestMessage: x.requestMessage
        }
      });

      const fuzzcontextId = updatedFCSList[0].fuzzcontextId;

      let jsonFCSUpdated: string = JSON.stringify(updatedFCSList);
      
      // base64 encode to easily transport via GraphQL as single string
      jsonFCSUpdated = btoa(jsonFCSUpdated)

      const [ok, error] =  await this.webclient.saveFuzzCaseSets(fuzzcontextId, jsonFCSUpdated); //await this.fuzzermanager.saveFuzzCaseSetSelected(newFCS);

      if(!ok)
        {
          this.toastError(error, 'Update Fuzz Cases');
        }
        else
        {
          // get latest updated fuzzcontext
          this.eventemitter.emit("onFuzzCaseSetUpdated", this.fuzzContextId);

          this.isTableDirty = false;
          
          this.toastSuccess('Fuzz Cases are updated successfully', 'Update Fuzz Cases');
        }
    } catch (error) {
       this.toastError(error, 'Update Fuzz Cases');
    }
    finally{
      this.saveBtnDisabled = false;
    }
  }

  onFuzzContextDeleted(fuzzcontextId) {

    this.clearData();
  }

  onFuzzContextRefreshClicked() {
    this.clearData();
  }

  public async getFuzzCaseSet_And_RunSummaries(fuzzcontextId: string, fuzzCaseSetRunsId: string)
  {
     this.isDataLoadingInProgress = true;

     try {
        const [ok, error, result] = await this.webclient.getApiFuzzCaseSetsWithRunSummaries(fuzzcontextId, fuzzCaseSetRunsId);
     
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
     finally {
        this.fuzzOnceDisabled = false;
        this.isDataLoadingInProgress = false;
     } 
  }

  async onFuzzContextSelected(fuzzcontextId, hostname, port)
  {
    this.selectedFuzzContextId = fuzzcontextId;
    this.selectedFuzzCaseSetRunId = '';
    this.selectedFuzzCaseSetId = '';

     this.hostname = hostname;
     this.port = port;

     this.refreshHostnameDisplay();

     await this.getFuzzCaseSet_And_RunSummaries(this.selectedFuzzContextId, '');
  }

  async onFuzzCaseSetRunSelected(fuzzcontextId: string, fuzzCaseSetRunsId: string, hostname, port)
  {
    this.selectedFuzzContextId = fuzzcontextId;
    this.selectedFuzzCaseSetRunId = fuzzCaseSetRunsId;
    this.selectedFuzzCaseSetId = '';

    this.hostname = hostname;
    this.port = port;

    this.refreshHostnameDisplay();

    await this.getFuzzCaseSet_And_RunSummaries(fuzzcontextId, fuzzCaseSetRunsId);
  }
  
  async onFuzzOnce(fuzzcontextId, fuzzcasesetId) {
    try {

      this.fuzzOnceDisabled = true;

      const [ok, error, caseSetRunSummaryId] = await this.webclient.fuzzOnce(fuzzcontextId, fuzzcasesetId)

    this.selectedFuzzCaseSetRunId = caseSetRunSummaryId;
    this.selectedFuzzContextId = fuzzcontextId;
    this.selectedFuzzCaseSetId = fuzzcasesetId;
      
    } catch (error) {
        this.$logger.error(error);
    }
  }

  async onRowClick(fcsrs: ApiFuzzCaseSetsWithRunSummaries) {

    this.selectedFuzzContextId = fcsrs.fuzzcontextId;
    this.selectedFuzzCaseSetId = fcsrs.fuzzCaseSetId;
    this.selectedFuzzCaseSetRunId = fcsrs.fuzzCaseSetRunId;


    if(this.isFuzzingInProgress()) {
      this.intervalGetReqRespDataOnFuzz();
      return;
    }

    if (!this.rowClickEnabled) {
        return;
    }

      this.rowClickEnabled = false;

      

      // send event to FuzzResult panel to display request and response
      this.eventemitter.emit("onFuzzCaseSetSelected", fcsrs.fuzzCaseSetId, fcsrs.fuzzCaseSetRunId);

      if (fcsrs.hostname != '') {
        this.hostname = fcsrs.hostname;
        this.port = fcsrs.port;
        this.refreshHostnameDisplay();
      }

    await Utils.delay(2000);   // spam click prevention

    this.rowClickEnabled = true;
  }

  async parseRequestMessage(rqMsg) {
    if(rqMsg == ''){
      return;
    }
    const [ok, error] = await this.webclient.parseRequestMessage(btoa(rqMsg));

    if(!ok) {
      this.requestMsgHasError = true;
      this.requestMsgErrorMessage = error;
      this.toastError(error);
      return;
    }
    this.requestMsgErrorMessage = '';
    this.requestMsgHasError = false;
  }

  async onDialogClose() {
    if (this.rqInEditOriginal != this.rqInEdit) {
      this.isTableDirty = true;

       this.fcsRunSums.map((fcs: ApiFuzzCaseSetsWithRunSummaries) => {
        if (fcs.fuzzCaseSetId == this.currentEditFuzzCaseSetId ) {
            fcs.requestMessage = this.rqInEdit;
        }
      });
    }
    this.currentEditFuzzCaseSetId = ''
    this.rqInEditOriginal = ''
    this.rqInEdit = '';
  }

  selectAllChanged(event) {
    this.fcsRunSums.forEach((fcs: ApiFuzzCaseSetsWithRunSummaries) => {
      fcs.selected = this.selectAll;
    });
    this.isTableDirty = true;
  }

  shortenValueInTable(bodyJson, length=40)
  {
    return Utils.shortenStr(bodyJson, length);
  }

  clearData() {
    this.clearIntervalGetReqRespData();
    
    this.currentFuzzingContextId = '';
    this.currentFuzzingCaseSetRunId = '';
    this.selectedFuzzContextId = '';
    this.selectedFuzzCaseSetId = '';
    this.selectedFuzzCaseSetRunId = '';

    this.fcsRunSums = [];
    this.hostname = '';
    this.port = -1;
    this.selectedRow = ''

    this.refreshHostnameDisplay();
  }

  isFuzzingInProgress() {
    if(this.currentFuzzingContextId != '' &&  this.currentFuzzingCaseSetRunId != '') {
      return true;
    }
    return false;
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
 