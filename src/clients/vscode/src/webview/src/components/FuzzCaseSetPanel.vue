
<!-- https://primefaces.org/primevue/treetable/responsive -->

<template>
  <v-card
    color="white"
    outlined
    style="display: flex; flex-flow: column; height: 97%;">
  
  <!-- request message editor for update fuzz context -->
  <Dialog v-model:visible="showHttpReqMsgEditDialog" 
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


      <div style="height: 15px;"></div>
      
      <div class="container-fluid">
        <div class="row" style="border: 1px solid grey">
            <div class="col" >
              <span style="text-align:center; width: 100%;" >Variables (readonly)</span>
              <textarea class="mt-2" readonly style="resize: none; width: 100%;height:100%" :value="fcsRunFuzzContext.templateVariables">
              </textarea>
            </div>
            <div class="col-9">
              <codemirror
                v-model="rqInEdit"
                placeholder="request message goes here..."
                :style="{ height: '500px' }"
                :autofocus="true"
                :indent-with-tab="true"
                :tab-size="2"
                :extensions="extensions"
                @ready="onCMReady" 
              />
            </div>
        </div>
      </div> 
      
  </Dialog>

  <Sidebar v-model:visible="showFullValueSideBar" position="right" style="width:700px;" :modal="true" :dismissable="true">
    <v-card
    color="white"
    outlined
    style="display: flex; flex-flow: column; height: 100%;">
      
      <div class="container-fluid" style="overflow-y:scroll">
        <div class="row">
          <div>
            URL
          </div>
          <div>
            <textarea :value="fuzzcasesetViewInSideBar.url" rows="6"
            style="height:100%; overflow=scroll;resize: none;" class="form-control"
            spellcheck="false" wrap="on" autocorrect="off" autocapitalize="off"
            />
          </div>
        </div>

        <div class="row">&nbsp;</div>

        <div class="row">
          <div>
            Header
          </div>
          <div>
            <textarea :value="fuzzcasesetViewInSideBar.header" rows="6"
            style="height:100%; overflow=scroll;resize: none;" class="form-control"
            spellcheck="false" wrap="on" autocorrect="off" autocapitalize="off"
            />
          </div>
        </div>

        <div class="row">&nbsp;</div>

        <div class="row">
          <div>
            Body
          </div>
          <div>
            <textarea :value="fuzzcasesetViewInSideBar.body" rows="13"
            style="height:100%; overflow=scroll;resize: none;" class="form-control"
            spellcheck="false" wrap="on" autocorrect="off" autocapitalize="off"
            />
          </div>
        </div>

        <div class="row">
          <div>
            myfile content
          </div>
          <div>
            <textarea :value="fuzzcasesetViewInSideBar.fileNonTemplate" rows="10"
            style="height:100%; overflow=scroll;resize: none;" class="form-control"
            spellcheck="false" wrap="on" autocorrect="off" autocapitalize="off"
            />
          </div>
        </div>

        <div class="row">&nbsp;</div>
      </div>
    </v-card>
  </Sidebar>

    <v-toolbar card color="#F6F6F6" flat density="compact" dense height="50px">
      <v-toolbar-title>Discovered API</v-toolbar-title>
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
    <!-- <input class="form-control input-sm" type="text" style="height:27px;" v-model="hostnameDisplay" readonly> -->
      <v-table density="compact" fixed-header height="350px" hover="true" >
        <thead>
          <tr>
            <th class="checkbox">
              <div class="form-check">
                <v-checkbox v-tooltip="'select for fuzzing'" color="cyan" id="flexCheckDefault" label="All" v-model="selectAll" density="compact" @change="(
                  selectAllChanged($event))"  hide-details />
              </div>
            </th>
            
            <!-- <th >
            </th> -->

            <th class="viewall">
            </th>

            <!-- <th >
            </th> -->

            <th class="settings">
            </th>
            
            <th class="verb">
              Verb
            </th>
            <th class="url">
              URL
            </th>
            <th class="filetype">
              File Type
            </th>
            <th class="httpcode">
              2xx
            </th>
            <th class="httpcode">
              3xx
            </th>
            <th class="httpcode">
              4xx
            </th>
            <th class="httpcode">
              5xx
            </th>
            <th class="httpcode">
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
            @click="(selectedRow= item.fuzzCaseSetId)"
            :style="item.fuzzCaseSetId === selectedRow ? 'background-color:lightgrey;' : ''">

            <!--checkbox-->
            <td>
              <div class="form-check">
                <v-checkbox color="cyan" id="flexCheckDefault" label="" v-model="item.selected" density="compact" @click="isTableDirty=true"  hide-details />
              </div>
            </td>

            <td>
              <v-icon
                  v-show="item.fuzzCaseSetRunId != ''"
                  style="cursor:pointer"
                  icon = "mdi-eye"
                  color="cyan"
                  class="m-0 p-0"
                  size="small"
                  v-tooltip="'all result'"
                  @click="(onRowClick(item), selectedRow= item.fuzzCaseSetId)"
                >
                </v-icon>
            </td>
            
            <!--settings-->
            <td>
              <div class="btn-group" style="cursor: pointer">
                  <v-icon
                  variant="flat"
                  icon="mdi-cog-outline"
                  color="cyan darken-3"
                  size="x-small"
                  data-bs-toggle="dropdown">
                  </v-icon>
                  <ul class="dropdown-menu dropdown-menu-end">
                    <li><button class="dropdown-item" type="button" 
                    @click="(
                      showFuzzCaseSetInSideBar(item)
                    )"
                    >View Full</button></li>

                    <li><button class="dropdown-item" type="button" 
                    :disabled="(isFuzzingInProgress())"
                    @click="(
                      showHttpReqMsgEditDialog = true,
                      rqInEdit = item.requestMessage,
                      rqInEditOriginal = item.requestMessage,
                      currentEditFuzzCaseSetId = item.fuzzCaseSetId
                    )"
                    >Edit Request Message</button></li>

                    <li><button class="dropdown-item" type="button"
                    :hidden="(isFuzzingInProgress() || selectedFuzzCaseSetRunId !='')"
                    @click="(
                        onFuzzOnce(this.selectedFuzzContextId, item.fuzzCaseSetId)
                      )"
                    >Fuzz Once</button></li>
                  </ul>
                </div>
            </td>
            
            <!--verb-->
            <td>
              <v-icon
                    :hidden="!(item.isGraphQL)"
                    variant="flat"
                    icon="mdi-graphql"
                    color="purple darken-3"
                    size="x-small"
                    class="m-0 p-0"
                    >
                </v-icon>
                <v-icon
                    :hidden="(item.isGraphQL)"
                    variant="flat"
                    icon="mdi-web"
                    color="purple darken-3"
                    size="x-small"
                    class="m-0 p-0"
                    >
                </v-icon>
              {{ item.verb }}
            </td>

            <!--url-->
            <td>
              <span>
                <v-tooltip
                :text="(item.urlNonTemplate)"
                activator="parent"
                max-width="500"
                max-height="500" />
                {{ shortenValueInTable(item.urlNonTemplate, 40) }}
              </span>
            </td>
            
            <td>
              {{item.file}}
            </td>
            <td>
              <a href="#" class="font-weight-bold text-info" v-if="item.http2xx > 0" @click="onFilterBy2xxClicked(item)"> {{ item.http2xx == undefined ? 0 : (item.http2xx) }} </a>
              <span v-else :class="item.http2xx > 0 ? 'font-weight-bold': ''">
                  {{ item.http2xx == undefined ? 0 : (item.http2xx) }} 
              </span>
            </td>
            <td>
              <a href="#" class="font-weight-bold text-info" v-if="item.http3xx > 0" @click="onFilterBy3xxClicked(item)"> {{ item.http3xx == undefined ? 0 : item.http3xx }} </a>
              <span v-else :class="item.http3xx > 0 ? 'font-weight-bold': ''">
                  {{ item.http3xx == undefined ? 0 : item.http3xx }}
              </span>
            </td>
            <td>
              <a href="#" class="font-weight-bold text-info" v-if="item.http4xx > 0" @click="onFilterBy4xxClicked(item)"> {{ item.http4xx == undefined ? 0 : item.http4xx }} </a>
              <span v-else :class="item.http4xx > 0 ? 'font-weight-bold': ''">
                {{ item.http3xx == undefined ? 0 : item.http4xx }}
              </span>
            </td>
            <td>
              <a href="#" class="font-weight-bold text-info" v-if="item.http5xx > 0" @click="onFilterBy5xxClicked(item)"> {{ item.http5xx == undefined ? 0 : item.http5xx }} </a>
              <span v-else :class="item.http5xx > 0 ? 'font-weight-bold': ''">
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
import { ApiFuzzCaseSetsWithRunSummaries, ApiFuzzCaseSetsWithRunSummariesFuzzContext } from '../Model';
import FuzzerWebClient from "../services/FuzzerWebClient";
import FuzzerManager from "../services/FuzzerManager";
import InputText from 'primevue/inputtext';
import RequestMessageExampleView from './RequestMessageExampleView.vue';
import { Util } from '@microsoft/applicationinsights-common';

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

  fcsRunFuzzContext: ApiFuzzCaseSetsWithRunSummariesFuzzContext;

  //array has to be a property by itself as live update of fuzz-stats are not able to for nested array in fcsRunFuzzContext
  fcsRunSums: Array<ApiFuzzCaseSetsWithRunSummaries| any> = [];

  showHttpReqMsgEditDialog = false;
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

 fuzzcasesetViewInSideBar = {
                        url: '',
                        header: '',
                        body: '',
                        fileNonTemplate: ''
                      };

  fuzzerConnected = false;

  currentFuzzContextId = '';

  fuzzContextId = '';
  fuzzCaseSetRunsId = '';

  // hostname = '';
  // port = -1;
  // hostnameDisplay = ''

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
    return;
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
    this.fuzzcasesetViewInSideBar = val
  }


  mounted(){
    //event from master
    this.eventemitter.on('fuzz.start', this.onFuzzStart);
    this.eventemitter.on('fuzz.stop', this.onFuzzStop);
    this.eventemitter.on('fuzzer.ready', this.onFuzzerReady);
    this.eventemitter.on('fuzzer.notready', this.onFuzzerNotReady);

    // listen to ApiDiscovery Tree item select event
    this.eventemitter.on("onFuzzContextSelected", this.onFuzzContextSelected);
    this.eventemitter.on("onFuzzCaseSetRunSelected", this.onFuzzCaseSetRunSelected);
    this.eventemitter.on("onFuzzCaseRunDeleted", this.onFuzzCaseRunDeleted);
    
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
  }

  onFuzzStop() {

    if(!this.isFuzzingInProgress()) {
      return;
    }

    this.currentFuzzingContextId = '';
    this.currentFuzzingCaseSetRunId = ''
  }

  onFuzzerReady() {
    this.fuzzerConnected = true;
  }

  onFuzzerNotReady() {
    this.clearData()
    this.fuzzerConnected = false;

    this.currentFuzzContextId = '';
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
      const tplVarB64e = btoa(this.fcsRunFuzzContext.templateVariables)

      const [ok, error] =  await this.webclient.saveFuzzCaseSets(fuzzcontextId, jsonFCSUpdated, tplVarB64e); //await this.fuzzermanager.saveFuzzCaseSetSelected(newFCS);

      if(!ok)
        {
          this.toastError(error, 'Update Fuzz Cases');
        }
        else
        {
          // get latest updated fuzzcontext
          //this.eventemitter.emit("onFuzzCaseSetUpdated", this.fuzzContextId);

          await this.getFuzzCaseSet_And_RunSummaries(this.selectedFuzzContextId, '');

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
          this.fcsRunFuzzContext = result;
          this.fcsRunSums =  this.fcsRunFuzzContext.fcsRunSums;
        }
      }
     } 
     finally {
        this.fuzzOnceDisabled = false;
        this.isDataLoadingInProgress = false;
     } 
  }

  async onFuzzContextSelected(fuzzcontextId)
  {
    this.selectedFuzzContextId = fuzzcontextId;
    this.selectedFuzzCaseSetRunId = '';
    this.selectedFuzzCaseSetId = '';

     await this.getFuzzCaseSet_And_RunSummaries(this.selectedFuzzContextId, '');
  }

  onFuzzCaseRunDeleted(fuzzCaseSetRunId) {
      if (fuzzCaseSetRunId == this.selectedFuzzCaseSetRunId) {
        this.clearData();
      }
    }

  async onFuzzCaseSetRunSelected(fuzzcontextId: string, fuzzCaseSetRunsId: string)
  {
    this.selectedFuzzContextId = fuzzcontextId;
    this.selectedFuzzCaseSetRunId = fuzzCaseSetRunsId;
    this.selectedFuzzCaseSetId = '';

    // this.hostname = hostname;
    // this.port = port;

    //this.refreshHostnameDisplay();

    await this.getFuzzCaseSet_And_RunSummaries(fuzzcontextId, fuzzCaseSetRunsId);
  }
  
  async onFuzzOnce(fuzzcontextId, fuzzcasesetId) {

    let caseSetRunSummaryId = '';

    try {

      this.fuzzOnceDisabled = true;

      const [ok, error, csrSummary] = await this.webclient.fuzzOnce(fuzzcontextId, fuzzcasesetId);

      caseSetRunSummaryId = csrSummary;

      this.selectedFuzzCaseSetRunId = caseSetRunSummaryId;
      this.selectedFuzzContextId = fuzzcontextId;
      this.selectedFuzzCaseSetId = fuzzcasesetId;
        
      } catch (error) {
          this.$logger.error(error);
      }
      finally {
        this.eventemitter.emit('fuzz.once.stop');
        await this.getFuzzCaseSet_And_RunSummaries(fuzzcontextId, caseSetRunSummaryId);
      }
  }

  async onRowClick(fcsrs: ApiFuzzCaseSetsWithRunSummaries) {

    this.selectedFuzzContextId = fcsrs.fuzzcontextId;
    this.selectedFuzzCaseSetId = fcsrs.fuzzCaseSetId;
    this.selectedFuzzCaseSetRunId = fcsrs.fuzzCaseSetRunId;

    if (!this.rowClickEnabled) {
        return;
    }

    this.rowClickEnabled = false;

    // send event to FuzzResult panel to display request and response
    this.eventemitter.emit("onFuzzCaseSetSelected", fcsrs.fuzzCaseSetId, fcsrs.fuzzCaseSetRunId, -1);

    await Utils.delay(2000);   // spam click prevention

    this.rowClickEnabled = true;
  }

  async onFilterBy2xxClicked(fcsrs: ApiFuzzCaseSetsWithRunSummaries) {

    try {

      if (!this.rowClickEnabled) {
        return;
      }

      this.rowClickEnabled = false;

      // send event to FuzzResult panel to display request and response
      this.eventemitter.emit("onFuzzCaseSetSelected", fcsrs.fuzzCaseSetId, fcsrs.fuzzCaseSetRunId, 299);

      await Utils.delay(2000);   // spam click prevention
      
    } catch (error) {
        this.$logger.error(error)
    }
    finally {
      this.rowClickEnabled = true;
    }
    
  }

  async onFilterBy3xxClicked(fcsrs: ApiFuzzCaseSetsWithRunSummaries) {

    try {

      if (!this.rowClickEnabled) {
        return;
      }

      this.rowClickEnabled = false;

      // send event to FuzzResult panel to display request and response
      this.eventemitter.emit("onFuzzCaseSetSelected", fcsrs.fuzzCaseSetId, fcsrs.fuzzCaseSetRunId, 399);

      await Utils.delay(2000);   // spam click prevention
      
    } catch (error) {
        this.$logger.error(error)
    }
    finally {
      this.rowClickEnabled = true;
    }
    
  }

  async onFilterBy4xxClicked(fcsrs: ApiFuzzCaseSetsWithRunSummaries) {

    try {

      if (!this.rowClickEnabled) {
        return;
      }

      this.rowClickEnabled = false;

      // send event to FuzzResult panel to display request and response
      this.eventemitter.emit("onFuzzCaseSetSelected", fcsrs.fuzzCaseSetId, fcsrs.fuzzCaseSetRunId, 499);

      await Utils.delay(2000);   // spam click prevention
      
    } catch (error) {
        this.$logger.error(error)
    }
    finally {
      this.rowClickEnabled = true;
    }
    
  }

  async onFilterBy5xxClicked(fcsrs: ApiFuzzCaseSetsWithRunSummaries) {

    try {

      if (!this.rowClickEnabled) {
        return;
      }

      this.rowClickEnabled = false;

      // send event to FuzzResult panel to display request and response
      this.eventemitter.emit("onFuzzCaseSetSelected", fcsrs.fuzzCaseSetId, fcsrs.fuzzCaseSetRunId, 599);

      await Utils.delay(2000);   // spam click prevention
      
    } catch (error) {
        this.$logger.error(error)
    }
    finally {
      this.rowClickEnabled = true;
    }
    
  }

  async parseRequestMessage(rqMsg) {
    if(rqMsg == ''){
      return;
    }

    rqMsg = `${this.fcsRunFuzzContext.templateVariables}\n${rqMsg}`

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

  showFuzzCaseSetInSideBar(item: ApiFuzzCaseSetsWithRunSummaries) {
    if(!item.isGraphQL) {
      this.fuzzcasesetViewInSideBar = {
                        url: item.urlNonTemplate,
                        header: Utils.jsonPrettify(item.headerNonTemplate),
                        body: Utils.jsonPrettify(item.bodyNonTemplate),
                        fileNonTemplate: item.fileNonTemplate
                      }
    }
    else {
      this.fuzzcasesetViewInSideBar = {
                        url: item.urlNonTemplate,
                        header: Utils.jsonPrettify(item.headerNonTemplate),
                        body: Utils.jsonPrettify(item.bodyNonTemplate + '\n\n' + item.graphQLVariableNonTemplate),
                        fileNonTemplate: item.fileNonTemplate
                      }
    }
                  
    this.showFullValueSideBar = true
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
    
    this.currentFuzzingContextId = '';
    this.currentFuzzingCaseSetRunId = '';
    this.selectedFuzzContextId = '';
    this.selectedFuzzCaseSetId = '';
    this.selectedFuzzCaseSetRunId = '';
    
    this.fcsRunFuzzContext = new ApiFuzzCaseSetsWithRunSummariesFuzzContext();
    this.fcsRunSums = [];

    this.selectedRow = ''

    this.isTableDirty = false;
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

table.table-fit {
    width: auto !important;
    table-layout: auto !important;
}
table.table-fit thead th, table.table-fit tfoot th {
    width: auto !important;
}
table.table-fit tbody td, table.table-fit tfoot td {
    width: auto !important;
}

th.checkbox {
  width: 7%
}

th.url {
  width: 21%
}

th.settings, th.viewall{
  width: 5%
}

th.verb {
  width: 7%
}

.v-tooltip__content.menuable__content__active {
  opacity: 1!important;
}

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
 