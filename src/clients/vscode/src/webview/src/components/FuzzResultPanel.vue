<template>
    <v-card
      color="white"
      outlined
      style="display: flex; flex-flow: column; height: 100%;"
      class="mt-2 border-1">

     <v-toolbar color="#F6F6F6" flat dense height="40px" width="100px" density="compact">
      <v-text-field
        color="cyan darken-3"
        hide-details
        clearable
        density="compact"
        label="search"
        height="20px"
        width="30px"
        single-line>
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
      <v-spacer></v-spacer>
    </v-toolbar>

    <Splitter  style="height: 100%" >
      <SplitterPanel :size="50">
        <v-table density="compact" fixed-header class="style=display: flex; flex-flow: column; height: 100%;">
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
              Duration
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in fdcsDataFiltered"
            :key="item.response.Id"
            @click="(onRowClick(item), selectedRow= item.response.Id)"
            :style="item.response.Id === selectedRow ? 'background-color:lightgrey;' : ''">


            <td>{{ item.response.statusCode }}</td>
            
            <td>
              {{ item.request.path }}
            </td>
            
            <td>
              {{shortenStringForDisplay(item.response.reasonPharse) }}
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
                  :value="selectedRequest"  rows="10" />
                </SplitterPanel>

                <SplitterPanel :size="50">
                  <textarea style="height:100%; overflowY=scroll;resize: none;" readonly class="form-control"
                  :value="selectedResponse"  rows="10" />
                </SplitterPanel>

            </Splitter>
          </SplitterPanel>
        </Splitter>
      </SplitterPanel>
    </Splitter>

    

   </v-card>
 
 </template>
 

<script lang="ts">

import { Options, Vue  } from 'vue-class-component';
import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';
import Dropdown from 'primevue/dropdown';
import { useToast } from "primevue/usetoast";
import FuzzerWebClient from "../services/FuzzerWebClient";
import FuzzerManager from "../services/FuzzerManager";
import Utils from "../Utils";
import { FuzzDataCase, FuzzRequest, FuzzResponse } from "../Model";

class Props {
  toast: any = {};
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
 

    toast = useToast();
    selectedRow = '';
    showDropDownStatusCodeFilter = false;

    selectedRequest = ''
    selectedResponse = '';

    fdcsDataOriginal: Array<FuzzDataCase> = [];
    fdcsDataFiltered: Array<FuzzDataCase> = [];
    fdcsFuzzingData: Array<FuzzDataCase> = [];
    unqStatusCodesFromFDCS: Array<string> = []

    mounted() {
      this.eventemitter.on("onFuzzCaseSetSelected", this.onFuzzCaseSetSelected);
    }

    async onFuzzCaseSetSelected(fuzzCaseSetId, fuzzCaseSetRunId) {

      if(Utils.isNothing(fuzzCaseSetId) || Utils.isNothing(fuzzCaseSetRunId)) {
        //this.toast.add({severity:'error', summary: '', detail:'fuzzcontextId or fuzzCaseSetRunId is missing in FuzzResultPanel ', life: 5000})
        return;
      }

      const [ok, error, result] = await this.fuzzermanager.getFuzzRequestResponse(fuzzCaseSetId, fuzzCaseSetRunId)

      if(!ok) {
        this.toast.add({severity:'error', summary: 'Fuzz Result Panel', detail:'error', life: 5000})
      }

      if (!ok || Utils.isNothing(result) || Utils.isLenZero(result)) {
          return;
      }

      this.fdcsDataOriginal = result;
      this.fdcsDataFiltered = this.fdcsDataOriginal;

      this.buildStatusCodesDropDown()
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

      this.selectedRequest = fcs.request.requestMessage;
      this.selectedResponse = fcs.response.responseDisplayText;
    }

    shortenStringForDisplay(str: string) {
      return Utils.shortenStr(str, 20);
    }

    onTblHeaderStatusCodeClicked() {
        this.showDropDownStatusCodeFilter = true;
    }

    timeDiff(a: string, b: string) {
       const aDate: Date = new Date(a);
       const bDate: Date = new Date(b);

       const value_start = a.split(':');
       const value_end = b.split(':');

      aDate.setHours(+value_start[0], +value_start[1], +value_start[2], 0);
      bDate.setHours(+value_end[0], +value_end[1], +value_end[2], 0);

       const diff = (new Date(bDate)).getTime() - (new Date(aDate)).getTime(); // millisecond 

       return diff;
    }
 }
 
 </script>
 
 <!-- Add "scoped" attribute to limit CSS to this component only -->
 <style scoped>

table.dropdowns-opened tbody tr.non-dropdown th {
    z-index: 0;
}

 </style>
 