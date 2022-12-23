<template>

    <v-card
      color="white"
      outlined
      style="display: flex; flex-flow: column; height: 100%;"
      class="mt-2 border-1">
     
     
     <v-toolbar color="#F6F6F6" flat dense height="30px" width="100px" density="compact">
      <!-- <input class="form-control form-control-sm" type="text" style="width=30px;" aria-label=".form-control-sm example" /> -->
      <v-text-field
        class="form-control-sm"
        color="cyan darken-3"
        hide-details
        clearable
        dense 
        density="compact"
        label="search"
        height="20px"
        solo>
        <template v-slot:prepend-inner>
        <v-icon
          color="cyan darken-3"
          icon="mdi-magnify"
        /> 
      </template>
      </v-text-field>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-icon color="cyan darken-3">mdi-content-save-settings-outline</v-icon>
    </v-toolbar>

    <Splitter  style="height: 100%" >
      <SplitterPanel :size="50">
        <v-table density="compact" fixed-header height="400px" hover="true" >          
        <thead>
          <tr>
            <th class="text-left">
              <div >
                Status Code
              </div>
            </th>
            <th class="text-left">
              Path
            </th>
            <th class="text-left">
              Reason
            </th>
            <th class="text-left">
              Request Content Length
            </th>
            <th class="text-left">
              Response Content Length
            </th>
            <th class="text-left">
              Duration(secs)
            </th>
          </tr>
          <tr v-show="isDataLoadingInProgress">
            <th colspan="6">
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
            v-for="item in fdcsDataFiltered"
            :key="item.response.Id"
            @click="(onRowClick(item), selectedRow= item.request.Id)"
            :style="item.request.Id === selectedRow ? 'background-color:lightgrey;' : ''">


            <td>{{ item.response.statusCode }}</td>
            
            <td>
              {{ shortenValueInTable(item.request.path, 15) }}
            </td>
            
            <td>
              {{shortenValueInTable(item.response.reasonPharse, 15) }}
            </td>

            <td>
              {{ item.request.contentLength }}
            </td>

            <td>
              {{ item.response.contentLength }}
            </td>

            <td>
              {{ timeDiff(item.request.requestDateTime, item.response.responseDateTime) }}
            </td>
            
          </tr>
        </tbody>
      </v-table>
      </SplitterPanel>

      <SplitterPanel :size="50">
        <Splitter gutterSize="0" layout="vertical">
          <SplitterPanel>
            <Splitter layout="vertical">

                <SplitterPanel :size="50">
                  <textarea style="height:100%; overflowY=scroll;resize: none;" readonly class="form-control"
                  :value="selectedRequest" />
                </SplitterPanel>

                <SplitterPanel :size="50">
                  <textarea style="height:100%; overflowY=scroll;resize: none;" readonly class="form-control"
                  :value="selectedResponse" />
                </SplitterPanel>

            </Splitter>
          </SplitterPanel>
        </Splitter>
      </SplitterPanel>
    </Splitter>

    

   </v-card>
 
 </template>
 

<script lang="ts">

import { inject } from 'vue';
import Logger from '../Logger';
import { Options, Vue  } from 'vue-class-component';
import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';
import Dropdown from 'primevue/dropdown';
import FuzzerWebClient from "../services/FuzzerWebClient";
import FuzzerManager from "../services/FuzzerManager";
import Utils from "../Utils";
import { FuzzDataCase, FuzzRequest, FuzzResponse } from "../Model";


class Props {
  toastInfo: any = {};
  toastError: any = {};
  toastSuccess: any = {};
  eventemitter: any = {};
  fuzzermanager: FuzzerManager;
  webclient : FuzzerWebClient;
}

@Options({
  components: {
    Splitter,
    SplitterPanel,
    Dropdown
  },
  watch: {

  }
})

 export default class FuzzResultPanel extends Vue.with(Props) {

    $logger: Logger|any;
    isDataLoadingInProgress = false;
    selectedRow = '';
    showDropDownStatusCodeFilter = false;

    selectedRequest = ''
    selectedResponse = '';

    dataCache = {};
    fdcsDataOriginal: Array<FuzzDataCase> = [];
    fdcsDataFiltered: Array<FuzzDataCase> = [];
    fdcsFuzzing: Array<FuzzDataCase> = [];
    unqStatusCodesFromFDCS: Array<string> = []
    
    currentFuzzingFuzzContextId = ''
    currentFuzzingFuzzCaseSetRunId = ''

    beforeMount() {
      this.$logger = inject('$logger');   
    }

    mounted() {
      //this.eventemitter.on('fuzzer.ready', this.onFuzzStartReady);
      this.eventemitter.on('fuzzer.notready', this.onFuzzNotReady);
      this.eventemitter.on("onFuzzCaseSetSelected", this.onFuzzCaseSetSelected);
      this.eventemitter.on("onFuzzContextSelected", this.clearData);
      this.eventemitter.on("onFuzzContextRefreshClicked", this.clearData)

      //fuzzing data event stream
      this.eventemitter.on('fuzz.update.fuzzdatacase', this.onFuzzDataCaseReceived);
    }

    onFuzzNotReady() {
      this.clearData();
    }

    onFuzzStart(data) {

      const fuzzContextId = data.fuzzContextId;
      const fuzzCaseSetRunId = data.fuzzCaseSetRunId;

      this.currentFuzzingFuzzContextId = fuzzContextId;
      this.currentFuzzingFuzzCaseSetRunId = fuzzCaseSetRunId;
  }

    onFuzzComplete(){
      this.currentFuzzingFuzzContextId = '';
      this.currentFuzzingFuzzCaseSetRunId = ''
      this.moveFuzzingDataBucketToOriginal();
    }

    onFuzzCancel(){
      this.currentFuzzingFuzzContextId = '';
      this.currentFuzzingFuzzCaseSetRunId = ''
      this.moveFuzzingDataBucketToOriginal();
    }

    //to determine this usage
    isFuzzing() {
      if (!Utils.isNothing(this.currentFuzzingFuzzContextId) && !Utils.isNothing(this.currentFuzzingFuzzCaseSetRunId) ) {
        return true;
      }
      return false;
    }

    // after fuzzing, move the fuzzing data array back to fdcsDataOriginal
    moveFuzzingDataBucketToOriginal() {
      this.fdcsDataOriginal = this.fdcsFuzzing;
      this.fdcsDataFiltered = [...this.fdcsDataOriginal]
      this.fdcsFuzzing = [];  //empty fuzzing data
    }

    storeFuzzDataCase(fdcs:  Array<FuzzDataCase|any>) {
      this.fdcsDataOriginal = fdcs;
      this.fdcsDataFiltered = [...this.fdcsDataOriginal]; //clone array
    }

    onFuzzDataCaseReceived(fdc: FuzzDataCase) {
      this.fdcsFuzzing.push(fdc);
    }

    async onFuzzCaseSetSelected(fuzzCaseSetId, fuzzCaseSetRunId) {

      try {
          //check if selected caseSetRunId is currently in fuzzing mode,
          //if yes do not retrieve data as fuzzer is sending data over websocket
          if(fuzzCaseSetId == this.currentFuzzingFuzzContextId && fuzzCaseSetRunId == this.currentFuzzingFuzzCaseSetRunId) {
            return;
          }

          if(Utils.isNothing(fuzzCaseSetId) || Utils.isNothing(fuzzCaseSetRunId)) {
            //this.toast.add({severity:'error', summary: '', detail:'fuzzcontextId or fuzzCaseSetRunId is missing in FuzzResultPanel ', life: 5000})
            this.$logger.errorMsg('fuzzCaseSetId and fuzzCaseSetRunId are empty when fuzz-case-set is selected', 'onFuzzCaseSetSelected');
            return;
          }

          this.isDataLoadingInProgress = true;

          const cacheKey = this.getCacheKey(fuzzCaseSetId, fuzzCaseSetRunId)

          //check if cache has the data
          if (cacheKey in this.dataCache){
            const fcsd = this.dataCache[cacheKey];
            this.storeFuzzDataCase(fcsd);
            return;
          }

          const [ok, error, result] = await this.fuzzermanager.getFuzzRequestResponse(fuzzCaseSetId, fuzzCaseSetRunId)

          if(!ok) {
            this.toastError(error, 'Fuzz Result Panel');
          }

          if (!ok || Utils.isNothing(result) || Utils.isLenZero(result)) {
              return;
          }

          this.storeFuzzDataCase(result);

          this.dataCache[cacheKey] = result;

          this.buildStatusCodesDropDown();
      }
      catch(error) {
        this.$logger.error(error);
      }
      finally {
        this.isDataLoadingInProgress = false;
      }
      
      
    }

    buildStatusCodesDropDown() {

      function onlyUnique(value, index, self) {
        return self.indexOf(value) === index;
      }

      const allSC =  this.fdcsDataFiltered.map(x => {
          return x.response.statusCode;
      });

      const unqSC = allSC.filter(onlyUnique);

      this.unqStatusCodesFromFDCS = unqSC;
    }

    onRowClick(fcs: FuzzDataCase) {
      
      if (fcs.request.invalidRequestError != '') {
        this.selectedRequest = fcs.request.invalidRequestError;
      } else {
        this.selectedRequest = Utils.b64d(fcs.request.requestMessage);
      }
      
      if(fcs.response.Id != null) {
        this.selectedResponse = Utils.b64d(fcs.response.responseDisplayText);
      }
    }

    //clear data on fuzz-context change but leave "fdcsFuzzing" alone
    clearData() {
        this.fdcsDataOriginal = [];
        this.fdcsDataFiltered = [];
        this.selectedRequest = '';
        this.selectedResponse = '';
    }

    shortenStringForDisplay(str: string) {
      return Utils.shortenStr(str, 20);
    }

    onTblHeaderStatusCodeClicked() {
        this.showDropDownStatusCodeFilter = true;
    }

    timeDiff(a: string, b: string) {

      if(b == null) {
        return 0;
      }

       const aDate: Date = new Date(a);
       const bDate: Date = new Date(b);

       var seconds = (bDate.getTime() - aDate.getTime()) / 1000;

       return parseFloat(seconds.toFixed(2));
    }

    shortenValueInTable(bodyJson, length=40)
    {
      return Utils.shortenStr(bodyJson, length);
    }

    getCacheKey(fuzzContextId: string, fuzzCasetSetRunId: string) {
      return fuzzContextId + '_' + fuzzCasetSetRunId;
    }
 }
 
 </script>
 
 <!-- Add "scoped" attribute to limit CSS to this component only -->
 <style scoped>

table.dropdowns-opened tbody tr.non-dropdown th {
    z-index: 0;
}

.loader-container {
 
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  width: 100%;
  height: 100%;
}

.loader {
  z-index: 3;
  border: 16px solid #f3f3f3;
  border-radius: 50%;
  border-top: 16px solid #3498db;
  width: 120px;
  height: 120px;
  -webkit-animation: spin 2s linear infinite;
  /* Safari */
  animation: spin 2s linear infinite;
}

 </style>
 