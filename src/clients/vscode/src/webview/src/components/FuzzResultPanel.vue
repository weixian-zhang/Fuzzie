<template>

    <v-card
      color="white"
      outlined
      style="display: flex; flex-flow: column; height: 100%;"
      class="mt-2 border-1">
     
     <!--view text in full Side Bar-->
     <Sidebar v-model:visible="showRequestValueSideBar" position="right" style="width:700px;">
      <TabView>
        <!--raw request message -->
        <TabPanel header="Message">
          <v-textarea auto-grow
                  outlined
                  rows="1"
                  readonly
                  v-model="tableRequestValueSideBar" />
        </TabPanel>

        <!--request path -->
        <TabPanel header="Path">
          <v-textarea auto-grow
                  outlined
                  rows="1"
                  readonly
                  v-model="tableRequestPathSideBar" />
        </TabPanel>

        <!--request querystring -->
        <TabPanel header="Querystring">
          <v-textarea auto-grow
                  outlined
                  rows="1"
                  readonly
                  v-model="tableRequestQSSideBar" />
        </TabPanel>

        <!--request headers -->
        <TabPanel header="Headers">
          <v-textarea auto-grow
                  outlined
                  rows="1"
                  readonly
                  v-model="tableRequestHeaderSideBar" />
        </TabPanel>

        <!--request body -->
        <TabPanel header="Body">
          <v-textarea auto-grow
                  outlined
                  rows="1"
                  readonly
                  v-model="tableRequestBodySideBar" />
        </TabPanel>

        <TabPanel header="Fuzzing Files">
          <v-table  density="compact" fixed-header height="430" hover="true" >          
            <tbody>
              <tr v-for="item in fuzzingUploadedFiles"
              :key="item.Id">
                <td>{{ item.fileName }}</td>
                <td><a href="#" @click="downloadFuzzFile(item.Id, item.fileName)">download </a></td>
              </tr>
            </tbody>
          </v-table>
        </TabPanel>
      </TabView>      
    </Sidebar>

    <Sidebar v-model:visible="showResponseValueSideBar" position="right" style="width:700px;">
      <TabView>
        <TabPanel header="Message">
          <v-textarea auto-grow
                  outlined
                  rows="1"
                  readonly
                  v-model="tableResponseValueSizeBar" />
        </TabPanel>
        <TabPanel header="Header">            
            <v-textarea auto-grow
                  outlined
                  rows="1"
                  readonly
                  v-model="tableResponseHeader" />
        </TabPanel>
        <TabPanel header="Body">            
            <v-textarea auto-grow
                  outlined
                  rows="1"
                  readonly
                  v-model="tableResponseBody" />
        </TabPanel>
        <TabPanel header="Reason">            
             <v-textarea auto-grow
                  outlined
                  rows="1"
                  readonly
                  v-model="tableResponseReasonPhrase" />
        </TabPanel>
      </TabView>      
    </Sidebar>

     
     <v-toolbar color="#F6F6F6" flat dense height="30px" width="100px" density="compact">
      <!-- <input class="form-control form-control-sm" type="text" style="width=30px;" aria-label=".form-control-sm example" /> -->
      <input type="text" class="form-control form-control-sm" id="colFormLabelSm" placeholder="search"
       v-model="fullTextSearchValue"
        @input="onfullTextSearchValueChange" />

      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>

    </v-toolbar>

    <Splitter  style="height: 100%" >
      <SplitterPanel :size="50">

        <v-table density="compact" fixed-header height="430" hover="true" >          
          <thead>
            <tr>
              <th class="text-left">
                  <div class="dropdown">
                    <button class="btn-sm btn-info btn-sm dropdown-toggle">Status Code</button>
                    <div class="dropdown-content">
                      <a href="#" 
                      v-for="item in unqStatusCodesFromFDCS"
                      :key="item"
                      @click="onStatusCodeFilterClicked(item)">
                        {{ item }}
                      </a>
                    </div>
                  </div>
              </th>
              <th class="text-left">
                Path
              </th>
              <th class="text-left">
                Reason
              </th>
              <th class="text-left">
                
                <div class="dropdown">
                    <button class="btn-sm btn-info btn-sm dropdown-toggle">Content Length(bytes)</button>
                    <div class="dropdown-content">
                      <v-radio-group inline v-model="tableFilterSmallerLarger" >
                        <v-radio
                          color="cyan"
                          label=">="
                          value=">="
                        ></v-radio>
                        <v-radio
                          color="cyan"
                          label="<="
                          value="<="
                        ></v-radio>
                      </v-radio-group>
                      <input type="number" id="typeNumber" class="form-control" @input="oncontentLengthInputChange"  step="20" v-model="contentLengthInputValue" />
                      <!-- <button class="btn-sm btn-info btn-sm dropdown-toggle"
                        @click="onContentLengthFilterClicked()">
                        Filter
                      </button> -->
                    </div>                 
                  </div>
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
                <span>
                  {{ shortenValueInTable(item.request.path, 15) }}
                </span>
              </td>
              
              <td>
                <span v-tooltip="item.response.reasonPharse">
                {{shortenValueInTable(item.response.reasonPharse, 15) }}
                </span>
              </td>

              <td>
                {{ item.response.contentLength }}
              </td>

              <td>
                {{ getTimeDiff(item.request.datetime, item.response.datetime) }}
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
                  <v-btn
                    width="100%"
                    size="x-small"
                    color="cyan"
                    @click="(
                      selectedRequest != '' ? (
                    tableRequestValueSideBar=selectedRequest,
                    settableRequestPathSideBar(),
                    setTableRequestQSSizeBar(),
                    setTableRequestHeadersSizeBar(),
                    setTableRequestBodySizeBar(),
                    showRequestValueSideBar = true) : ''
                  )">
                  Request
                  </v-btn>
                  <textarea style="height:100%; overflowY=scroll;resize: none;" readonly class="form-control"
                  :value="selectedRequest" />
                </SplitterPanel>

                <SplitterPanel :size="50">
                  <v-btn
                    width="100%"
                    size="x-small"
                    color="cyan"
                    @click="(
                      selectedResponse != '' ?
                    (tableResponseValueSizeBar=selectedResponse,
                    setTableResponseHeader(),
                    setTableResponseReasonPhrase(),
                    setTableResponseBody(),
                    showResponseValueSideBar = true) : ''
                  )">
                  Response
                  </v-btn>
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
import { FuzzDataCase, FuzzRequestFileUpload_ViewModel, FuzzRequest, FuzzRequestResponseMessage_ViewModel } from "../Model";
import Sidebar from 'primevue/sidebar';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';

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
    Dropdown,
    Sidebar,
    TabView,
    TabPanel
  },
  watch: {

  }
})



 export default class FuzzResultPanel extends Vue.with(Props) {

    $logger: Logger|any;
    isDataLoadingInProgress = false;
    selectedRow = '';
    showDropDownStatusCodeFilter = false;

    selectedReqRespMessage: FuzzRequestResponseMessage_ViewModel;
    selectedRequest = ''
    selectedResponse = '';

    //dataCache = {};
    fdcsDataOriginal: Array<FuzzDataCase|any> = [];
    fdcsDataFiltered: Array<FuzzDataCase|any> = [];
    //fdcsFuzzing = {};
    unqStatusCodesFromFDCS: Array<string> = []
    fuzzingUploadedFiles: Array<FuzzRequestFileUpload_ViewModel> = []
    
    showRequestValueSideBar = false;

    tableRequestValueSideBar = '';
    tableRequestPathSideBar = '';
    tableRequestQSSideBar = '';
    tableRequestHeaderSideBar = '';
    tableRequestBodySideBar = '';
    tableResponseReasonPhrase = '';
    tableResponseHeader = '';
    tableResponseBody= '';

    showResponseValueSideBar = false;
    tableResponseValueSizeBar = ''

    fullTextSearchValue = '';

    contentLengthInputValue = 100;
    tableFilterSmallerLarger = '>=';
    
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
      this.eventemitter.on("onFuzzCaseSetRunSelected", this.clearData);
      this.eventemitter.on("onFuzzContextRefreshClicked", this.clearData)

      //fuzzing data event stream
      this.eventemitter.on('fuzz.start', this.onFuzzStart);
      this.eventemitter.on('fuzz.stop', this.onFuzzStop);
      //this.eventemitter.on('fuzz.update.fuzzdatacase', this.onFuzzDataCaseReceived);

      
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

    onFuzzStop(){
      this.currentFuzzingFuzzContextId = '';
      this.currentFuzzingFuzzCaseSetRunId = ''
      //this.switchFuzzingDataBucketToOriginal();
    }

    //switchOriginalToFuzzingDataBucket(fuzzCaseSetId) {
        //const fuzzingData: FuzzDataCase[] = this.fdcsFuzzing[fuzzCaseSetId];
        //this.fdcsDataFiltered = fuzzingData;
        //this.fdcsDataOriginal = [];
    //}

    // after fuzzing, move the fuzzing data array back to fdcsDataOriginal
    //switchFuzzingDataBucketToOriginal() {
      //this.fdcsDataOriginal = [...this.fdcsDataFiltered]
      //this.fdcsFuzzing = {};  //empty fuzzing data
    //} 

    storeFuzzDataCase(fdcs:  Array<FuzzDataCase|any>) {
      this.fdcsDataOriginal = fdcs;
      this.fdcsDataFiltered = [...this.fdcsDataOriginal]; //clone array
    }

    //onFuzzDataCaseReceived(fdc: FuzzDataCase) {
      //const list = this.fdcsFuzzing[fdc.fuzzCaseSetId]
      //if(list == undefined) {
          //this.fdcsFuzzing[fdc.fuzzCaseSetId] = []
      //}
      //this.fdcsFuzzing[fdc.fuzzCaseSetId].push(fdc);
   // }

   onStatusCodeFilterClicked(httpStatusCode) {

    if (this.fdcsDataOriginal == undefined || this.fdcsDataOriginal.length == 0) {
          return;
    }

      this.fdcsDataFiltered = this.fdcsDataOriginal.filter(x => {
        if(x != undefined && x.response != undefined  && x.response.statusCode == httpStatusCode) {
          return x;
        }
      });
   }

   oncontentLengthInputChange(input) {
      //const contentLengthToFilter = input.data;

      try {
        if (this.fdcsDataOriginal == undefined || this.fdcsDataOriginal.length == 0) {
          return;
        }

        var operator = '>=';

        if (this.tableFilterSmallerLarger == '>=') {
          this.fdcsDataFiltered = this.fdcsDataOriginal.filter(x => {
            if(x != undefined && x.response.contentLength >= this.contentLengthInputValue) {
              return x;
            }
          });
        }
        else {
          this.fdcsDataFiltered = this.fdcsDataOriginal.filter(x => {
            if(x != undefined && x.response.contentLength <= this.contentLengthInputValue) {
              return x;
            }
          });
        }
      }
      catch(error) {
        this.$logger.error(error)
      }
  
    }

    async onFuzzCaseSetSelected(fuzzCaseSetId, fuzzCaseSetRunId) {

      try {

          if(this.isDataLoadingInProgress) {
            return;
          }
          
          //check if selected caseSetRunId is currently in fuzzing mode,
          //if yes do not retrieve data as fuzzer is sending data over websocket
          //if(this.isFuzzingInProgress() && this.currentFuzzingFuzzCaseSetRunId == fuzzCaseSetRunId) {
            //this.switchOriginalToFuzzingDataBucket(fuzzCaseSetId);
            //return;
          //}

          if(Utils.isNothing(fuzzCaseSetId) || Utils.isNothing(fuzzCaseSetRunId)) {
            //this.toast.add({severity:'error', summary: '', detail:'fuzzcontextId or fuzzCaseSetRunId is missing in FuzzResultPanel ', life: 5000})
            this.$logger.errorMsg('fuzzCaseSetId and fuzzCaseSetRunId are empty when fuzz-case-set is selected', 'onFuzzCaseSetSelected');
            return;
          }

          this.isDataLoadingInProgress = true;

          //this.clearSelectedReqResp();

          //const cacheKey = this.getCacheKey(fuzzCaseSetId, fuzzCaseSetRunId)

          //check if cache has the data
          //if (cacheKey in this.dataCache){
            //const fcsd = this.dataCache[cacheKey];
            //this.storeFuzzDataCase(fcsd);
            //return;
          //} 

          const [ok, error, result] = await this.webclient.getFuzzRequestResponse(fuzzCaseSetId, fuzzCaseSetRunId)

          if(!ok) {
            this.toastError(error, 'Fuzz Result Panel');
          }

          if (!ok || Utils.isNothing(result) || Utils.isLenZero(result)) {
            this.clearTableBindingData();
            return;
          }

          this.storeFuzzDataCase(result);

          //this.dataCache[cacheKey] = result;

          this.buildStatusCodesDropDown();
      }
      catch(error) {
        this.$logger.error(error);
      }
      finally {
        this.isDataLoadingInProgress = false;
      }
    }

    onfullTextSearchValueChange(input) {
      const searchText = input.data;

      if(this.fdcsDataOriginal.length == 0 || searchText == '' || searchText.length <= 2) {
        return;
      }

      //this.fdcsDataFiltered = this.fdcsDataOriginal.map(fdc => {

        //if (fdc.request.verb.indexOf(searchText) >= 0 || fdc.request.)
        //return fdc;
      //});

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

    async onRowClick(fcs: FuzzDataCase) {

      if (fcs.request.invalidRequestError != '') {
        this.selectedRequest = fcs.request.invalidRequestError;
        return;
      }

      //get request and response messages
      const [ok, error, result] = await this.webclient.get_request_response_messages(fcs.request.Id, fcs.response.Id)

      if(!ok) {
        this.selectedReqRespMessage = new FuzzRequestResponseMessage_ViewModel();
        this.selectedRequest = '';
        this.selectedResponse = '';
        return;
      }

      this.selectedReqRespMessage = result

      if(!Utils.isNothing(result.requestMessage)) {
        this.selectedRequest = Utils.b64d(result.requestMessage);
      }

      if(!Utils.isNothing(result.responseDisplayText)) {
        this.selectedResponse = Utils.b64d(result.responseDisplayText);
      }

      //get uploaded files
      const [fok, ferror, fresult] = await this.webclient.getFuzzingUploadedFiles(fcs.request.Id);

      if(!fok) {
        this.$logger.errorMsg(ferror);
        return;
      }

      this.fuzzingUploadedFiles = fresult;
    }

    async downloadFuzzFile(fuzzFileUploadId, fileName) {

      const content = await this.webclient.getFuzzFileContent(fuzzFileUploadId);

      if(content == '') {
        this.toastInfo('file content is empty');
      }

      const url = window.URL.createObjectURL(new Blob([content]));
      const link = document.createElement('a');
      link.href = url;
      link.target = "fileDownloader"; //arbitrary name of iframe
      link.setAttribute('download', `${fileName}`);
      document.body.appendChild(link);
      link.click(); 
    }

    settableRequestPathSideBar() {

      if (this.selectedReqRespMessage == undefined) {
        return;
      }

      const path = this.selectedReqRespMessage.requestPath;

      if (Utils.isNothing(path)) {
        this.tableRequestPathSideBar = '';
        return;
      }

      this.tableRequestPathSideBar = path;
    }

    setTableRequestQSSizeBar() {

      if (this.selectedReqRespMessage == undefined) {
        return;
      }

      const qs = this.selectedReqRespMessage.requestQuerystring;

      try {
        if (Utils.isNothing(qs)) {
          this.tableRequestQSSideBar = '';
          return;
        }

        this.tableRequestQSSideBar = qs; //qs.split('?').join('? \n').split('&').join('& \n');
      }
      catch (error) {
          this.tableRequestQSSideBar = qs;
      }
      
    }

    setTableRequestHeadersSizeBar() {
      
      if (this.selectedReqRespMessage == undefined) {
        return;
      }

      const headersStr = this.selectedReqRespMessage.requestHeader;

      try{
        if (Utils.isNothing(headersStr)) {
          this.tableRequestHeaderSideBar = '';
          return;
        }

        if(Utils.jsonTryParse(headersStr)) {
          this.tableRequestHeaderSideBar = JSON.stringify(JSON.parse(headersStr), null, 2)
        }
        else {
          this.tableRequestHeaderSideBar = headersStr;
        }
        
      }
      catch (error) {
          this.tableRequestHeaderSideBar = headersStr;
      }

    }
    setTableRequestBodySizeBar() {

      try {
        
        if (this.selectedReqRespMessage == undefined) {
          return;
        }

        var body = this.selectedReqRespMessage.requestBody;

        if (Utils.isNothing(body)) {
          this.tableRequestBodySideBar = '';
          return;
        }

        body = atob(body);

        if(Utils.jsonTryParse(body)) {
            this.tableRequestBodySideBar = JSON.stringify(JSON.parse(body), null, 2)
          }
          else {
            this.tableRequestBodySideBar = body;
          }
      }
      catch(error) {
        this.$logger.error(error);
        this.tableRequestBodySideBar = '';
      }
    }

    setTableResponseReasonPhrase() {

      if (this.selectedReqRespMessage == undefined) {
        return;
      }

      const reason = this.selectedReqRespMessage.responseReasonPhrase;

      if (Utils.isNothing(reason)) {
        this.tableResponseReasonPhrase = '';
        return;
      }

      this.tableResponseReasonPhrase = reason;
    }

    setTableResponseHeader() {

      if (this.selectedReqRespMessage == undefined) {
        return;
      }

      const header = this.selectedReqRespMessage.responseHeader;

      if (Utils.isNothing(header)) {
        this.tableResponseHeader = '';
        return;
      }

      if(Utils.jsonTryParse(header)) {
          this.tableResponseHeader = JSON.stringify(JSON.parse(header), null, 2)
        }
        else {
          this.tableResponseHeader = header;
        }
    }

    setTableResponseBody(selectedRequest: FuzzRequest) {

      if (this.selectedReqRespMessage == undefined) {
        return;
      }

      var body = this.selectedReqRespMessage.responseBody;

      if (Utils.isNothing(body)) {
        this.tableResponseBody = '';
        return;
      }

      body = atob(body);

      if(Utils.jsonTryParse(body)) {
          this.tableResponseBody = JSON.stringify(JSON.parse(body), null, 2)
        }
        else {
          this.tableResponseBody = body;
        }
    }

    //clear data on fuzz-context change but leave "fdcsFuzzing" alone
    clearData() {
      this.tableRequestValueSideBar = '';
      this.tableRequestPathSideBar = '';
      this.tableRequestQSSideBar = '';
      this.tableRequestHeaderSideBar = '';
      this.tableRequestBodySideBar = '';
      this.tableResponseReasonPhrase = '';
      this.tableResponseHeader = '';
      this.tableResponseBody= '';

      this.clearTableBindingData();
      this.clearSelectedReqResp();
    }

    clearTableBindingData() {
      this.fdcsDataFiltered = [];
      this.fdcsDataOriginal = [];
    }

    clearSelectedReqResp() {
      this.selectedReqRespMessage = new FuzzRequestResponseMessage_ViewModel();
      this.selectedRequest = '';
      this.selectedResponse = '';
    }

    shortenStringForDisplay(str: string) {
      return Utils.shortenStr(str, 20);
    }

    onTblHeaderStatusCodeClicked() {
        this.showDropDownStatusCodeFilter = true;
    }

    getTimeDiff(a: string, b: string) {

      if(b == null) {
        return 0;
      }

       var startDate = new Date(a);
      // Do your operations
      var endDate   = new Date(b);
      var seconds = (endDate.getTime() - startDate.getTime()) / 1000;

       return parseFloat(seconds.toFixed(2));
    }

    shortenValueInTable(bodyJson, length=40)
    {
      return Utils.shortenStr(bodyJson, length);
    }

    //getCacheKey(fuzzContextId: string, fuzzCasetSetRunId: string) {
      //return fuzzContextId + '_' + fuzzCasetSetRunId;
    //}

    isFuzzingInProgress() {
        if(!Utils.isNothing(this.currentFuzzingFuzzContextId)  && !Utils.isNothing(this.currentFuzzingFuzzContextId)) {
          return true;
        }
        return false;
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

/* Dropdown Button */
.dropbtn {
  background-color: #04AA6D;
  color: white;
  padding: 16px;
  font-size: 16px;
  border: none;
}

/* The container <div> - needed to position the dropdown content */
.dropdown {
  position: relative;
  display: inline-block;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

/* Links inside the dropdown */
.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

/* Change color of dropdown links on hover */
.dropdown-content a:hover {background-color: #ddd;}

/* Show the dropdown menu on hover */
.dropdown:hover .dropdown-content {display: block;}

/* Change the background color of the dropdown button when the dropdown content is shown */
.dropdown:hover .dropbtn {background-color: #3e8e41;}

 </style>
 