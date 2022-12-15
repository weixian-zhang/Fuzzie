
<!-- https://primefaces.org/primevue/treetable/responsive -->

<template>
  <v-card
    color="white"
    outlined
    style="display: flex; flex-flow: column; height: 100%;">
  
  <Sidebar v-model:visible="showFullValueSideBar" position="right" style="width:500px;">
    <code >
      <v-textarea auto-grow
          outlined
          rows="1"
          readonly
          v-model="tableValViewInSizeBar" />
    </code>
  </Sidebar>

    <v-toolbar card color="lightgrey" flat dense height="50px">
      <v-toolbar-title>Fuzz Cases</v-toolbar-title>
      
      
        <v-btn v-tooltip.bottom="'save'" icon  variant="plain" height="30px" plain 
          :disabled="saveBtnDisabled"
          @click="(
            saveFuzzCaseSets
            )">
          <v-badge  color="pink" dot v-model="isTableDirty">
            <v-icon>mdi-content-save-settings-outline</v-icon>
          </v-badge>
        </v-btn>
      <v-btn v-tooltip.left="'start fuzzing'" icon  variant="plain" height="30px" plain >
        <v-icon>mdi-lightning-bolt</v-icon>
      </v-btn>
    </v-toolbar>
      
      <v-table density="compact" fixed-header height="350px" >
        <thead>
          <tr>
            <th class="text-left">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" id="flexCheckDefault" v-model="selectAll" 
                @change="(
                  selectAllChanged($event))">
                <label class="form-check-label" for="flexCheckDefault">
                  All
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
            @click="onRowClick(item)">
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

  </v-card>

</template>
      

<script lang="ts">
import { Options, Vue  } from 'vue-class-component';
// import { Watch } from 'vue-property-decorator'
import DataTable from 'primevue/datatable';
import Sidebar from 'primevue/sidebar';
import Utils from '../Utils';
import { ApiFuzzCaseSetsWithRunSummaries } from '../Model';
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
    DataTable,
    Sidebar
  },
  watch: {

  }
})

 export default class FuzzCaseSetPanel extends Vue.with(Props) {


  fcsRunSums: Array<ApiFuzzCaseSetsWithRunSummaries> = [];

  dataCache = {};

  selectAll = true;

  showTable = true;

  saveBtnDisabled = false;

  showFullValueSideBar = false;

  isTableDirty = false;

  tableValViewInSizeBar = '';

  toast = useToast();

  // @Watch('fcsRunSums', { immediate: true, deep: true })
  // onCaseSetSelectionChanged(val: ApiFuzzCaseSetsWithRunSummaries, oldVal: ApiFuzzCaseSetsWithRunSummaries) {
  //   console.log(val);
  //   return;
  // }

  onTableValueSeeInFullClicked(jsonValue) {
      this.tableValViewInSizeBar = JSON.stringify(JSON.parse(jsonValue),null,'\t')
  }

  onTableValueNonJsonSeeInFullClicked(val) {
    this.tableValViewInSizeBar = val
  }

  beforeMount() {
    return;
  }
  
  mounted(){
    // listen to ApiDiscovery Tree item select event
    this.eventemitter.on("onFuzzContextSelected", this.onFuzzContextSelected)
    this.eventemitter.on("onFuzzContextDelete", this.onFuzzContextDeleted)

    //websocket receive message from fuzzer

  }


  async saveFuzzCaseSets() {

    if(!this.isTableDirty) {
      this.toast.add({severity:'info', summary: '', detail:'no changes to save', life: 5000});
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
        this.toast.add({severity:'error', summary: 'Update Fuzz Cases', detail:error, life: 5000});
      }
      else
      {
        this.isTableDirty = false;
        this.toast.add({severity:'success', summary: 'Update Fuzz Cases', detail:'Fuzz Cases are updated successfully', life: 5000});
      }

    this.saveBtnDisabled = false;
  }

  onFuzzContextDeleted(fuzzcontextId) {
      if( fuzzcontextId in this.dataCache)
      {
        delete this.dataCache[fuzzcontextId];

        if(this.fcsRunSums.length > 0)
        {
            if(this.fcsRunSums[0].fuzzcontextId == fuzzcontextId)
            {
              this.fcsRunSums = [];
            }
        }
      }
  }

  async onFuzzContextSelected(fuzzcontextId: string, fuzzCaseSetRunsId: string)
  {
    if(fuzzCaseSetRunsId == undefined) {
      fuzzCaseSetRunsId = ''
    }
    
    const key = fuzzcontextId.concat(fuzzCaseSetRunsId);

    const fcsList: Array<ApiFuzzCaseSetsWithRunSummaries> = this.dataCache[key];

    if(fcsList != undefined && Array.isArray(fcsList) == true && fcsList.length > 0)
    {
      this.fcsRunSums = this.dataCache[fuzzcontextId];
    }
    else
    {
      const [ok, error, result] = await this.fuzzermanager.getApiFuzzCaseSetsWithRunSummaries(fuzzcontextId, fuzzCaseSetRunsId);

      if(!ok)
      {
        this.toast.add({severity:'error', summary: 'Get Fuzz Cases', detail:error, life: 5000});
      }
      else
      {
        this.dataCache[key] = result;
        this.fcsRunSums = this.dataCache[key];
      }
    }
  }

  onRowClick(fcsrs) {
    return;
  }

  selectAllChanged(event) {
    this.fcsRunSums.forEach(fcs => {
      fcs.selected = this.selectAll;
    });
    this.isTableDirty = true;
  }

  shortenJsonValueInTable(bodyJson, length=100)
  {
    const pj = Utils.prettifyJson(bodyJson);
    if(pj != undefined && pj.length > length)
    {
      return pj.substring(0, length) + "...";
    }
    else
    {
      return pj;
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

code {
  font-family: Consolas,"courier new";
  color: crimson;
  background-color: #f1f1f1;
  padding: 2px;
  font-size: 105%;
}
 </style>
 