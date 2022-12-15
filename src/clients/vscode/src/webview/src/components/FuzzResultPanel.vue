<template>
    <v-card
      color="white"
      outlined
      style="display: flex; flex-flow: column; height: 100%;"
      class="mt-2 border-1">

     <!-- <v-toolbar color="lightgrey" flat dense height="50px">
      <v-spacer />
      <v-btn icon height="30px" width="30px">
        <v-icon>mdi-card-plus</v-icon>
      </v-btn>
    </v-toolbar> -->

    <Splitter  style="height: 100%" >
      <SplitterPanel :size="60">
        <v-table density="compact" fixed-header height="350px" >
        <thead>
          <tr>
            <th class="text-left">
              Path
            </th>
            <th class="text-left">
              Status Code
            </th>
            <th class="text-left">
              Reason
            </th>
            <th class="text-left">
              Content Length
            </th>
            <th class="text-left">
              Duration
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
            @click="onRowClick(item)"
            :class="key === selectedRow ? 'custom-highlight-row' : ''">
            <td>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" v-model="item.selected" 
                @click="isTableDirty=true">
              </div>

            </td>
            <td>{{ item.verb }}</td>
            
            <td>
              <span style="cursor: pointer" @click="(
                onTableValueNonJsonSeeInFullClicked(item.path),
                showFullValueSideBar = true
              )">
                {{ item.path }}
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
      </SplitterPanel>

      <SplitterPanel :size="40">
        <Splitter gutterSize="0" layout="vertical">
          <SplitterPanel>
            <Splitter layout="vertical">

                <SplitterPanel :size="50">
                  request
                </SplitterPanel>

                <SplitterPanel :size="50">
                  response
                </SplitterPanel>

            </Splitter>
          </SplitterPanel>
        </Splitter>
      </SplitterPanel>
    </Splitter>

    

   </v-card>
 
 </template>
 
<script lang="ts">

import { Options, Vue } from 'vue-class-component';
import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';
import { useToast } from "primevue/usetoast";
import FuzzerWebClient from "../services/FuzzerWebClient";
import FuzzerManager from "../services/FuzzerManager";

class Props {
  // optional prop
  eventemitter: any = {}
  fuzzermanager: FuzzerManager
  webclient : FuzzerWebClient
}

@Options({
  components: {
    Splitter,
    SplitterPanel
  },
  watch: {

  }
})

 export default class FuzzResultPanel extends Vue {

  toast = useToast();


 
 }
 
 </script>
 
 <!-- Add "scoped" attribute to limit CSS to this component only -->
 <style scoped>

 </style>
 