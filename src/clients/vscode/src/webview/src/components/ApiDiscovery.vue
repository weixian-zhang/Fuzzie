<!-- https://pictogrammers.github.io/@mdi/font/6.9.96/ -->

<template>


    
    <v-card
    color="white"
    outlined
    height="420px"
    >

    <v-toolbar card color="cyan" flat dense height="50px">
      <v-btn  variant="plain" height="30px" plain icon v-tooltip.right="'refresh fuzz contexts'"
      :disabled="!isGetFuzzContextFinish"
        @click="getFuzzcontexts">
            <v-icon>mdi-refresh</v-icon>
      </v-btn>
      <v-spacer />
      <v-btn  variant="plain" height="30px" plain icon v-tooltip.bottom="'create new messaging fuzz context (in roadmap)'">
        <v-icon>mdi-message-plus-outline</v-icon>
      </v-btn>
      <v-btn v-tooltip.bottom="'create new API fuzz context'" icon  variant="plain" height="30px" plain  @click="newContextSideBarVisible = true">
        <v-icon>mdi-api</v-icon>
      </v-btn>
    </v-toolbar>

    <Tree :value="nodes" selectionMode="single" v-show="showTree" scrollHeight="420px" class="pa-1">
              <template #default="slotProps">
                <div v-on:click="onFuzzContextSelected(slotProps.node.key)">
                  [<v-icon
                  variant="flat"
                  icon="mdi-api"
                  color="primary"
                  width="15px"
                  height="15px"
                  ></v-icon>]
                  <b>{{slotProps.node.label}}</b>
                </div>
              </template>

              <!-- fuzz run -->
              <template #url="slotProps">
                  <span>
                    {{slotProps.node.label}}
                    <div v-show="slotProps.node.isFuzzing">
                      <b class="text-info">fuzzing</b>
                      <v-progress-linear
                          indeterminate
                          color="teal">
                      </v-progress-linear>
                    </div>
                  </span>
              </template>
          </Tree>

    
      
    </v-card>
</template>

<script lang="ts">

import { Options, Vue } from 'vue-class-component';
import FuzzerManager from '../services/FuzzerManager';
import Toast from 'primevue/toast';
import { useToast } from "primevue/usetoast";
import Tree, { TreeNode } from 'primevue/tree';
import dateformat from 'dateformat';
import Sidebar from 'primevue/sidebar';
import VSCodeMessager, {Message} from '../services/VSCodeMessager';
import Utils from '../Utils';
import { ApiFuzzContext } from '../Model';

class Props {
  // optional prop
  eventemitter: any = {}
  vscodeMsger: VSCodeMessager;
}

@Options({
  components: {
    Tree,
    Sidebar,
    Toast
  },
})


export default class ApiDiscovery extends Vue.with(Props) {
  
  fm = new FuzzerManager();
  openapi3FileInputFileVModel: Array<any> = [];
  requestTextFileInputFileVModel: Array<any>  = [];
  showPasswordValue = false;
  nodes: TreeNode[] = [];
  showTree = this.nodes.length > 0 ? "true": "false";
  newContextSideBarVisible = false;
  isGetFuzzContextFinish = true;
  toast = useToast();

  securityBtnVisibility= {
    anonymous: false,
    basic: false,
    bearer: false,
    apikey: false

  }

  newApiContext= new ApiFuzzContext();

mounted() {
    this.getFuzzcontexts()

    //this.vscodeMsger.subscribe("file-content-result", this.readFileContentResult);
  }

  readFileContentResult(message)
  {
    const msgObj: Message = JSON.parse(message);

    if(msgObj.type == 'openapi')
    {
      console.log(msgObj.content);
    }
  }
  
  async getFuzzcontexts() {

    try {

      this.isGetFuzzContextFinish = false;
      const fcs = await this.fm.getFuzzcontexts()    

      if (fcs.length > 0)
      {
        this.nodes = this.createTreeNodesFromFuzzcontexts(fcs);
      }

      this.isGetFuzzContextFinish = true;
    } catch (error) {
        //TODO: log
        console.log(error)
    }
  }

  createTreeNodesFromFuzzcontexts(fcs): TreeNode[] {

    const nodes: TreeNode[] = [];

    fcs.forEach(fc => {

        const fcNode: any = {
          key: fc.Id,
          label: fc.name,
          data: fc
        };

        nodes.push(fcNode)

        fc.fuzzCaseSetRuns.forEach(fcsr => {

          const casesetNode = {
            key: fcsr.fuzzCaseSetRunsId,
            isFuzzing: false,
            label: dateformat(fcsr.startTime, "ddd, mmm dS, yyyy, h:MM:ss TT"), //`${nodeLabel.toLocaleDateString('en-us')} ${nodeLabel.toLocaleTimeString()}`,
            data: fcsr
          };
          
          if(fcNode.children == undefined)
          {
            fcNode.children = [];
          }

          fcNode.children.push(casesetNode);
        });
    });

    return nodes;

  }

  onFuzzContextSelected(fuzzContextId) {
    this.eventemitter.emit("onFuzzContextSelected", fuzzContextId);
  }

  async onRequestTextFileChange(event) {
    console.log(event);

    const files = event.target.files;

    const file = files[0];

    const reader = new FileReader();
    if (file.name.includes(".http") || file.name.includes(".fuzzie") || file.name.includes(".text")) {

      const content = await Utils.readFileAsText(file);
      this.newApiContext.requestTextContent = btoa(content);

      if(this.requestTextFileInputFileVModel != null && this.requestTextFileInputFileVModel.length > 0)
      {
        this.newApiContext.requestTextFilePath = this.requestTextFileInputFileVModel[0]?.name;
      }
    }
    else
    {
      this.requestTextFileInputFileVModel = [];
      this.toast.add({severity:'error', summary: 'Invalid File Type', detail:'Request Text file has ext of .http, .text or .fuzzie', life: 5000});
    }
  }

  async onOpenApi3FileChange(event) {
    console.log(event);

    const files = event.target.files;

    const file = files[0];

    const reader = new FileReader();
    if (file.name.includes(".yaml") || file.name.includes(".json")) {

      const content = await Utils.readFileAsText(file);
      this.newApiContext.openapi3Content = btoa(content);

      if(this.openapi3FileInputFileVModel != null && this.openapi3FileInputFileVModel.length > 0)
      {
        this.newApiContext.openapi3FilePath = this.openapi3FileInputFileVModel[0]?.name;
      }
    }
    else
    {
      this.openapi3FileInputFileVModel = [];
      this.toast.add({severity:'error', summary: 'Invalid File Type', detail:'OpenAPI3 spec files are yaml or json', life: 5000});
    }
  }

  async createNewApiContext() {
    
    this.newApiContext.authnType = this.determineAuthnType();
    if(this.newApiContext.authnType == 'Anonymous')
    {
      this.newApiContext.isanonymous = true;
    }
    else
    {
      this.newApiContext.isanonymous = false;
    }

    this.newApiContext.apiDiscoveryMethod = this.determineApiDiscoveryMethod();

    if(this.newApiContext.openapi3Content == '' && this.newApiContext.requestTextContent == '')
    {
      this.toast.add({severity:'error', summary: 'API Discovery', detail:'need either OpenAPI 3 spec or Request Text to create context', life: 5000});
      return;
    }

    if(this.newApiContext.name == '' || this.newApiContext.hostname == '' || this.newApiContext.port == '')
    {
      this.toast.add({severity:'error', summary: 'Missing Info', detail:'Name, hostname, port are required', life: 5000});
      return;
    }
   

    const result =  await this.fm.newFuzzContext(this.newApiContext);
    const ok = result['ok'];
    const error =result['error'];

    if(!ok && error != '')
    {
      this.toast.add({severity:'error', summary: 'Create new API context', detail:error, life: 5000});
      return;
    }
    else
    {
      this.toast.add({severity:'success', summary: 'API Fuzz Context created', detail:error, life: 3000});
    }
  }

  // Anonymous = "Anonymous",
  // Basic = "Basic",
  // Bearer = "Bearer",
  // ApiKey = "ApiKey"
  determineAuthnType(): string {

    if(this.newApiContext.isanonymous)
    {
      return "Anonymous";
    }
    else if(this.newApiContext.basicUsername != '' && this.newApiContext.basicPassword != '')
    {
       return "Basic";
    }
    else if(this.newApiContext.apikeyHeader != '' && this.newApiContext.apikey != '')
    {
       return  "ApiKey";
    }
    else if(this.newApiContext.bearerToken != '')
    {
       return  "Bearer";
    }

    return "Anonymous";
  }

  determineApiDiscoveryMethod(){
    if(this.newApiContext.requestTextContent != '')
    {
        return 'request-text';
    }
    return 'openapi3';
  }

  clearContextForm() {
    this.openapi3FileInputFileVModel = [];
    this.requestTextFileInputFileVModel = [];
    this.newApiContext = new ApiFuzzContext();
  }
}
</script>


<style scoped>
input[type=text]{
   padding:0px;
   margin-bottom:2px; /* Reduced from whatever it currently is */
   margin-top:2px; /* Reduced from whatever it currently is */
}


</style>
