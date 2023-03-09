<template>

    <v-card
      color="white"
      outlined
      style="display: flex; flex-flow: column; height: 100%;"
      class="">
     
     <!--view text in full Side Bar-->
     <Sidebar v-model:visible="showRequestValueSideBar" position="right" style="width:700px;">
      <TabView>
        <!--raw request message -->
        <TabPanel header="Message">
          <textarea 
                  style="height:100%; overflow=scroll;resize: none;" class="form-control"
                  outlined
                  rows="40"
                  readonly
                  spellcheck="false" wrap="on" autocorrect="off" autocapitalize="off"
                  v-model="tableRequestValueSideBar" />
        </TabPanel>

        <!--request path -->
        <TabPanel header="Path">
          <textarea
                  style="height:100%; overflow=scroll;resize: none;" class="form-control"
                  outlined
                  rows="40"
                  readonly
                  spellcheck="false" wrap="on" autocorrect="off" autocapitalize="off"
                  v-model="tableRequestPathSideBar" />
        </TabPanel>

        <!--request querystring -->
        <TabPanel header="Querystring">
          <textarea
                  style="height:100%; overflow=scroll;resize: none;" class="form-control"
                  outlined
                  rows="40"
                  readonly
                  spellcheck="false" wrap="on" autocorrect="off" autocapitalize="off"
                  v-model="tableRequestQSSideBar" />
        </TabPanel>

        <!--request headers -->
        <TabPanel header="Headers">
          <textarea 
                  style="height:100%; overflow=scroll;resize: none;" class="form-control"
                  outlined
                  rows="40"
                  readonly
                  spellcheck="false" wrap="on" autocorrect="off" autocapitalize="off"
                  v-model="tableRequestHeaderSideBar" />
        </TabPanel>

        <!--request body -->
        <TabPanel header="Body">
          <textarea 
                  style="height:100%; overflow=scroll;resize: none;" class="form-control"
                  outlined
                  rows="40"
                  readonly
                  spellcheck="false" wrap="off" autocorrect="off" autocapitalize="off"
                  v-model="tableRequestBodySideBar" />
        </TabPanel>

        <TabPanel header="Fuzzing Files">
          <v-table class="border-0"  density="compact" fixed-header height="430" hover="true" >          
            <tbody>
              <tr v-for="file in fuzzingUploadedFiles"
                :key="file.Id">
                <td>
                  <div > {{ file.fileName }}</div>
                  <span style="color: blue;cursor: pointer; text-decoration: underline;" 
                    @click="(downloadFuzzFile(file.Id, file.fileName))" >
                    download
                  </span>
                </td>
              </tr>
            </tbody>
          </v-table>
        </TabPanel>
      </TabView>      
    </Sidebar>
 <!-- downloadFuzzFile(file.Id, file.fileName))"> -->
    <Sidebar v-model:visible="showResponseValueSideBar" position="right" style="width:700px;">
      <TabView>
        <TabPanel header="Message">
          <textarea 
                  style="height:100%; overflow=scroll;resize: none;" class="form-control"
                  outlined
                  rows="40"
                  readonly
                  spellcheck="false" wrap="off" autocorrect="off" autocapitalize="off"
                  v-model="tableResponseValueSizeBar" />
        </TabPanel>
        <TabPanel header="Header">            
            <textarea 
                  style="height:100%; overflow=scroll;resize: none;" class="form-control"
                  outlined
                  rows="40"
                  readonly
                  spellcheck="false" wrap="on" autocorrect="off" autocapitalize="off"
                  v-model="tableResponseHeader" />
        </TabPanel>
        <TabPanel header="Body">            
            <textarea 
                  style="height:100%; overflow=scroll;resize: none;" class="form-control"
                  outlined
                  rows="40"
                  readonly
                  spellcheck="false" wrap="off" autocorrect="off" autocapitalize="off"
                  v-model="tableResponseBody" />
        </TabPanel>
        <TabPanel header="WebPage View">            
            <div v-html="tableResponseBody" />
        </TabPanel>
        <TabPanel header="Reason">            
             <textarea 
                  style="height:100%; overflow=scroll;resize: none;" class="form-control"
                  outlined
                  rows="40"
                  readonly
                  spellcheck="false" wrap="on" autocorrect="off" autocapitalize="off"
                  v-model="tableResponseReasonPhrase" />
        </TabPanel>
      </TabView>      
    </Sidebar>

     
     <v-toolbar color="#F6F6F6" flat dense height="30px" width="300px" density="compact">
      <!-- <input class="form-control form-control-sm" type="text" style="width=30px;" aria-label=".form-control-sm example" /> -->
      <!-- <input type="text" class="form-control form-control-sm" id="colFormLabelSm" placeholder="search"
       v-model="quickSearchTextValue"
        @input="onQuickSearchTextValueChange" /> -->

        <v-text-field
        full-width
        density="compact"
        variant="solo"
        label="search path, querystring and header"
        single-line
        hide-details
        clear-icon="mdi-close-circle"
        clearable
        v-model="quickSearchTextValue"
        @input="onQuickSearchTextValueChange"
        @click:clear="(this.fdcsDataFiltered = [...this.fdcsDataOriginal])"
        ></v-text-field>

      <!-- <v-spacer />

      <v-toolbar-title>Fuzz Result</v-toolbar-title>

      <v-spacer /> -->

      <v-spacer></v-spacer>
        <v-text-field
          full-width
          density="compact"
          variant="solo"
          label="search request and response body"
          single-line
          hide-details
          clear-icon="mdi-close-circle"
          clearable
          v-model="deepSearchTextValue"
          ></v-text-field>
          <v-btn
              icon
              color="cyan"
              @click="onDeepSearchClick"
            >
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
      

    </v-toolbar>

    <Splitter  style="height: 100%" >
      
      <SplitterPanel :size="50">
        <div class="container-fluid">
          <div class="row">
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
                    Content Length(response bytes)
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
          </div>
          <div class="row">
            <div class="col-8">
              <v-pagination
                density="compact"
                variant="flat"
                v-show="(fdcsDataFiltered.length > 0 && paginationTotalPages > 1)"
                v-model="paginationCurrentPage"
                :length="paginationTotalPages"
                :total-visible="8"
                :disabled="isDataLoadingInProgress"
              ></v-pagination>
              </div>
            <div class="col-4">
              <v-combobox
                v-show="(fdcsDataFiltered.length > 0 && paginationTotalPages > 8)"
                v-model="paginationCurrentPage"
                :items="paginationTotalPagesArray"
                :disabled="isDataLoadingInProgress"
                density="compact"
                label="select page"
              ></v-combobox>
              <!-- <div class="btn-group" style="width: 100px; position: static;"
               v-show="(fdcsDataFiltered.length > 0 && paginationTotalPages > 8)">
                <button type="button" class="btn btn-info btn-sm dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                  Page
                </button>
                <ul class="dropdown-menu">
                  <li 
                  v-for="p in paginationTotalPagesArray"
                  :key="p">
                    <a  class="dropdown-item" href="#"
                    @click="(getFuzzRequestResponse())"
                    >{{ p }}</a>
                  </li>
                </ul>
              </div> -->
            </div>
          </div>
        </div>
      </SplitterPanel>

      <SplitterPanel :size="50">
        <Splitter gutterSize="0" layout="vertical">
          <SplitterPanel>
            <Splitter layout="vertical">
                <SplitterPanel :size="50">
                  
                  <div v-show="isReqRespMessageDataLoading">
                    <v-progress-linear
                      indeterminate
                      rounded
                      color="cyan">
                    </v-progress-linear>
                  </div>

                  <v-btn
                    width="100%"
                    size="x-small"
                    color="cyan"
                    @click="(
                      selectedRequestMessage != '' ? (
                    tableRequestValueSideBar=selectedRequestMessage,
                    settableRequestPathSideBar(),
                    setTableRequestQSSizeBar(),
                    setTableRequestHeadersSizeBar(),
                    setTableRequestBodySizeBar(),
                    showRequestValueSideBar = true) : ''
                  )"
                    >
                  Request
                  </v-btn>
                  <textarea style="height:100%; overflow=scroll;resize: none;" readonly class="form-control" row="12" 
                  spellcheck="false" wrap="off" autocorrect="off" autocapitalize="off"
                  :value="(selectedRequestMessage)" />
                </SplitterPanel>

                <SplitterPanel :size="50">

                  <div v-show="isReqRespMessageDataLoading">
                    <v-progress-linear
                      indeterminate
                      rounded
                      color="cyan">
                    </v-progress-linear>
                  </div>

                  <v-btn
                    width="100%"
                    size="x-small"
                    color="cyan"
                    @click="(
                      selectedResponseDisplayText != '' ?
                    showResponseValueSideBar = true : '',
                    setResponseDisplayText(),
                    setTableResponseHeader(),
                    setTableResponseBody(),
                    setTableResponseReasonPhrase()
                    )"
                    >
                  Response
                  </v-btn>
                  <textarea style="height:100%; overflow=scroll;resize: none;" readonly row="10" class="form-control"
                  spellcheck="false" wrap="off" autocorrect="off" autocapitalize="off"
                  type="text" v-model="selectedResponseDisplayText"
                   />

                </SplitterPanel>

            </Splitter>
          </SplitterPanel>
        </Splitter>
      </SplitterPanel>
    </Splitter>

    

   </v-card>
 
 </template>
 

<script lang="ts">

/* tslint:disable */ 

import { inject, watch } from 'vue';
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
import VSCode from  '../VSCode';
import { Watch } from 'vue-property-decorator'

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

    vscode: VSCode;
    $logger: Logger|any;
    isDataLoadingInProgress = false;
    isReqRespMessageDataLoading = false;
    selectedRow = '';
    showDropDownStatusCodeFilter = false;

    selectedReqRespMessage: FuzzRequestResponseMessage_ViewModel;
    selectedRequestMessage = ''
    selectedResponseDisplayText = '';

    fdcsDataOriginal: Array<FuzzDataCase|any> = [];
    fdcsDataFiltered: Array<FuzzDataCase|any> = [];
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

    quickSearchTextValue = '';
    deepSearchTextValue = '';

    contentLengthInputValue = 100;
    tableFilterSmallerLarger = '>=';

    pollFuzzResultHandler: any = undefined;

    currentFuzzingFuzzContext = ''
    currentFuzzingFuzzCaseSetRun = ''

    paginationPageSize = 500;
    paginationCurrentPage = 0;
    paginationTotalPages = 1;
    paginationTotalPagesArray: Array<number> = [];

    fuzzCaseSetId = ''
    fuzzCaseSetRunId = ''

    

    beforeMount() {
      this.$logger = inject('$logger');
    }

    mounted() {

      watch(() => this.paginationCurrentPage, async (newVal, oldVal) => {
        await this,this.getFuzzRequestResponses();
      });

      this.vscode = new VSCode();

      //this.eventemitter.on('fuzzer.ready', this.onFuzzStartReady);
      this.eventemitter.on('fuzzer.notready', this.onFuzzNotReady);
      this.eventemitter.on("onFuzzCaseSetSelected", this.onFuzzCaseSetSelected);
      this.eventemitter.on("onFuzzContextSelected", this.clearData);
      this.eventemitter.on("onFuzzCaseSetRunSelected", this.clearData);
      this.eventemitter.on("onFuzzContextRefreshClicked", this.clearData)
      this.eventemitter.on("onFuzzCaseRunDeleted", this.onFuzzCaseRunDeleted)
      //fuzzing data event stream
      this.eventemitter.on('fuzz.start', this.onFuzzStart);
      this.eventemitter.on('fuzz.stop', this.onFuzzStop);
      
    }

    onFuzzNotReady() {
      this.clearData();
    }

    onFuzzStart(data) {
      this.currentFuzzingFuzzContext = data.fuzzContextId;
      this.currentFuzzingFuzzCaseSetRun = data.fuzzCaseSetRunId;
    }

    onFuzzStop(){
      if (this.pollFuzzResultHandler != undefined){
        clearInterval(this.pollFuzzResultHandler);
        this.pollFuzzResultHandler = undefined;
      }
      this.currentFuzzingFuzzContext ='';
      this.currentFuzzingFuzzCaseSetRun = '';
    }

    storeFuzzDataCase(fdcs:  Array<FuzzDataCase|any>) {
      this.fdcsDataOriginal = fdcs;
      this.fdcsDataFiltered = [...this.fdcsDataOriginal]; //clone array
    }

   onStatusCodeFilterClicked(httpStatusCode) {

    if (this.fdcsDataOriginal == undefined || this.fdcsDataOriginal.length == 0) {
          return;
    }

    // remove filter
    if(httpStatusCode == 'All') {
        this.fdcsDataFiltered = this.fdcsDataOriginal;
        return;
    }

      this.fdcsDataFiltered = this.fdcsDataOriginal.filter(x => {
        if(x != undefined && x.response != undefined  && x.response.statusCode == httpStatusCode) {
          return x;
        }
      });
   }

    onFuzzCaseRunDeleted(fuzzCaseSetRunId) {
      if (fuzzCaseSetRunId == this.fuzzCaseSetRunId) {
        this.clearData();
      }
    }

    async onFuzzCaseSetSelected(fuzzCaseSetId, fuzzCaseSetRunId, statusCode) {

      try {

          if(this.isDataLoadingInProgress) {
            return;
          }

          if(Utils.isNothing(fuzzCaseSetId) || Utils.isNothing(fuzzCaseSetRunId)) {
            //this.toast.add({severity:'error', summary: '', detail:'fuzzcontextId or fuzzCaseSetRunId is missing in FuzzResultPanel ', life: 5000})
            this.$logger.errorMsg('fuzzCaseSetId and fuzzCaseSetRunId are empty when fuzz-case-set is selected', 'onFuzzCaseSetSelected');
            return;
          }

          this.paginationCurrentPage = 0;

          this.paginationTotalPages = 1;

          this.paginationTotalPagesArray = [];

          this.fuzzCaseSetId = fuzzCaseSetId;
          
          this.fuzzCaseSetRunId = fuzzCaseSetRunId;

          await this.getFuzzRequestResponses(statusCode);
      }
      catch(error) {
        this.$logger.error(error);
      }
      //finally {
      //  this.isDataLoadingInProgress = false;
      //}
    }

    async getFuzzRequestResponses(statusCode = -1) {
      
      try
      {
        if (this.fuzzCaseSetId == '' || this.fuzzCaseSetRunId == '' ) {
          return;
        }

        if(this.isDataLoadingInProgress) {
          return;
        }

        this.isDataLoadingInProgress = true;

        const [ok, error, totalPages, result] = await this.webclient.getFuzzRequestResponse(
          this.fuzzCaseSetId, 
          this.fuzzCaseSetRunId, 
          statusCode,
          this.paginationPageSize, 
          this.paginationCurrentPage)

        if(!ok) {
          this.toastError(error, 'Fuzz Result Panel');
        }

        if (!ok || Utils.isNothing(result) || Utils.isLenZero(result)) {
          this.clearTableBindingData();
          return;
        }

        this.paginationTotalPages = totalPages;

        this.paginationTotalPagesArray = [];

        if (totalPages > 8) {
          for(var i = 1; i <= totalPages; i++){
            this.paginationTotalPagesArray.push(i);
          }
        }
        
        this.storeFuzzDataCase(result);

        this.buildStatusCodesDropDown();
      }
      catch(error){
        this.$logger.error(error);
        return;
      }
      finally {
        this.isDataLoadingInProgress = false;
      }
    }

    async onDeepSearchClick() {
      
      try{

          if (this.isDataLoadingInProgress || this.isFuzzingInProgress()) {
          this.toastInfo('Deep search is disabled when data loading or fuzzing is in progress');
          return;
          }

          if (this.fuzzCaseSetId == '' || this.fuzzCaseSetRunId == '' ) {
            return;
          }

          this.isDataLoadingInProgress = true;

          const searchText = this.deepSearchTextValue;

          if(searchText == null || this.fdcsDataOriginal.length == 0 || searchText == '' || searchText.length < 3) {
            return;
          }

          const [ok, err, fdcList] = await this.webclient.deepSearchBody(searchText, this.fuzzCaseSetId, this.fuzzCaseSetRunId)

          this.storeFuzzDataCase(fdcList);
      }
      catch(error) {
        this.$logger.error(error)
      }
      finally {
        this.isDataLoadingInProgress = false;
      }
    }

    async onPaginationPageChange(page) {
      try
      {
        await this.getFuzzRequestResponses();
      }
      catch (error) {
        this.$logger.error(error)
      }
    }

    onQuickSearchTextValueChange(input) {
      if (this.isDataLoadingInProgress || this.isFuzzingInProgress()) {
        this.toastInfo('Search is disabled when data loading or fuzzing is in progress');
        return;
      }

      const searchText = this.quickSearchTextValue;

      if(searchText == null || this.fdcsDataOriginal.length == 0 || searchText == '' || searchText.length < 3) {
        this.fdcsDataFiltered = [...this.fdcsDataOriginal];
        return;
      }

      this.fdcsDataFiltered = [...this.fdcsDataOriginal];

      this.fdcsDataFiltered = this.fdcsDataFiltered.filter((datacase: FuzzDataCase) => {
        if(
          datacase.request.path?.toLowerCase().includes(this.quickSearchTextValue) ||
          datacase.request.querystring?.toLowerCase().includes(this.quickSearchTextValue) ||
          datacase.request.headers?.toLowerCase().includes(this.quickSearchTextValue) ||
          datacase.response.headerJson?.toLowerCase().includes(this.quickSearchTextValue) ||
          datacase.response.reasonPharse?.toLowerCase().includes(this.quickSearchTextValue)
          ) {
          return true;
        }
        else {
          return false;
        }
      });

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

      this.unqStatusCodesFromFDCS = []
      this.unqStatusCodesFromFDCS.push('All')
      unqSC.forEach(x => {
        this.unqStatusCodesFromFDCS.push(x)
      })
      
    }

    async onRowClick(fcs: FuzzDataCase) {

      try {

        if (fcs.request.invalidRequestError != '') {
          this.selectedRequestMessage = fcs.request.invalidRequestError;
          return;
        }

        this.isReqRespMessageDataLoading = true;

        //get request and response messages
        const [ok, error, result] = await this.webclient.get_request_response_messages(fcs.request.Id, fcs.response.Id)

        if(!ok || Utils.isNothing(result)) {
          this.selectedReqRespMessage = new FuzzRequestResponseMessage_ViewModel();
          this.selectedRequestMessage = '';
          this.selectedResponseDisplayText = '';
          return;
        }

        this.selectedReqRespMessage = result;
        this.selectedRequestMessage = this.selectedReqRespMessage.requestMessage; //this.jsonPrettify(this.selectedReqRespMessage.requestMessage);
        this.selectedResponseDisplayText = result.responseDisplayText; //this.jsonPrettify(result.responseDisplayText);

        this.selectedReqRespMessage.responseBody = this.jsonPrettify(result.responseBody);

        //get uploaded files
        const [fok, ferror, fresult] = await this.webclient.getFuzzingUploadedFiles(fcs.request.Id);

        if(!fok) {
          this.$logger.errorMsg(ferror);
          return;
        }

        this.fuzzingUploadedFiles = fresult;

      }
      catch(error) {
        this.$logger.error(error, 'FuzzResultPanel.onRowClick');
      }
      finally {
        this.isReqRespMessageDataLoading = false;
      }
    }


    async downloadFuzzFile(fileId, fileName) {

      try {


        if (Utils.isNothing(fileId)) {
          this.$logger.error('File ID is not found when downloading fuzz-payloads')
          return;
        }

        var downloadedContent = await this.webclient.getFuzzFileContent(fileId);

        if(Utils.isNothing(downloadedContent)) {
          this.toastInfo('file content is empty');
          return;
        }

        //vscode extension save file
        this.vscode.saveFile(fileName, downloadedContent);

        //support browser testing
        if(this.vscode.isVSCodeAPIUndefined()) {
          const byteArrContent: any = this.stringToArrayBuffer(downloadedContent);
          const url = window.URL.createObjectURL(new Blob([byteArrContent]));
          const link = document.createElement('a');
          link.href = url;
          link.target = "fileDownloader"; //arbitrary name of iframe
          link.setAttribute('download', `${fileName}`);
          document.body.appendChild(link);
          link.click(); 
        }
      }
      catch(error) {
        this.$logger.error(error);
        this.toastError(error);
      }
    }

  stringToArrayBuffer(data) {
    var binaryLen = data.length;
    var bytes = new Uint8Array(binaryLen);
    for (var i = 0; i < binaryLen; i++) {
        var ascii = data.charCodeAt(i);
        bytes[i] = ascii;
    }
    return bytes;
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

        this.tableRequestBodySideBar = this.jsonPrettify(body);

        // if(Utils.jsonTryParse(body)) {
        //    this.tableRequestBodySideBar = JSON.stringify(JSON.parse(body), null, 2)
        //}
        //else {
        //    this.tableRequestBodySideBar = body;
        //} 
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

    setResponseDisplayText() {
      if (Utils.isNothing(this.selectedReqRespMessage)) {
        return;
      }

      this.tableResponseValueSizeBar = this.jsonPrettify(this.selectedReqRespMessage.responseDisplayText);
    }

    setTableResponseHeader() {

      if (Utils.isNothing(this.selectedReqRespMessage)) {
        return;
      }

      this.tableResponseHeader = this.jsonPrettify(this.selectedReqRespMessage.responseHeader);
    }

    setTableResponseBody() {

      if (this.selectedReqRespMessage == undefined) {
        return;
      }

      this.tableResponseBody = this.jsonPrettify(this.selectedReqRespMessage.responseBody);

    }

    //clear data on fuzz-context change but leave "fdcsFuzzing" alone
    clearData() {

      this.fuzzCaseSetId = '';
      this.fuzzCaseSetRunId = ''

      this.tableRequestValueSideBar = '';
      this.tableRequestPathSideBar = '';
      this.tableRequestQSSideBar = '';
      this.tableRequestHeaderSideBar = '';
      this.tableRequestBodySideBar = '';
      this.tableResponseReasonPhrase = '';
      this.tableResponseHeader = '';
      this.tableResponseBody= '';

      this.unqStatusCodesFromFDCS = []

      this.clearTableBindingData();
      this.clearSelectedReqResp();
    }

    clearTableBindingData() {
      this.fdcsDataFiltered = [];
      this.fdcsDataOriginal = [];
    }

    clearSelectedReqResp() {
      this.selectedReqRespMessage = new FuzzRequestResponseMessage_ViewModel();
      this.selectedRequestMessage = '';
      this.selectedResponseDisplayText = '';
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
        if(!Utils.isNothing(this.currentFuzzingFuzzContext)  && !Utils.isNothing(this.currentFuzzingFuzzContext)) {
          return true;
        }
        return false;
    }

    jsonPrettify(data: string) {

      if (Utils.isNothing(data)) {
        return '';
      }

      var dBody = data;

      if(Utils.jsonTryParse(data)) {
          dBody = JSON.stringify(JSON.parse(dBody), null, 2)
          return dBody;
      }

      return dBody;
      
    }
 }
 
 </script>
 
 <!-- Add "scoped" attribute to limit CSS to this component only -->
 <style scoped>

textarea
{
  width:100%;
  height:100%;
}

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
 