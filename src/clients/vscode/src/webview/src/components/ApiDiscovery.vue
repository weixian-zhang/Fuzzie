<!-- https://pictogrammers.github.io/@mdi/font/6.9.96/ -->

<template>
  <div>
    <Toast />
    <!-- new context -->
    <Sidebar v-model:visible="newContextSideBarVisible" position="right" style="width:950px;">
      
      <div class="container-fluid">
        <div class="row mb-3"><h5>Create new Fuzz Context</h5></div>
        <div class="row">
            <div class="col-6">
              <form>
                <div class="form-group">
                  <label for="contextName">Name</label>
                  <v-text-field
                    v-model="newContext.name"
                    :rules="rules"
                    counter="25"
                    hint="This field uses counter prop"
                    label="name"
                  ></v-text-field>

                  <!-- <input type="text" class="form-control form-control-sm" id="contextName"  placeholder="fuzz context name" v-model=""> -->
                </div>

              <v-divider />
              <b>Test Properties</b>
              <v-divider />

              <div class="form-group mb-3" >
                <v-text-field
                    v-model="newContext.hostname"
                    :rules="rules"
                    hint="hostname"
                    label="Hostname" />
                </div>

                <div class="form-group">
                  <v-text-field
                    v-model="newContext.port"
                    :rules="rules"
                    hint="port"
                    label="Port" />
                </div>

              <v-divider />
              <b>API Discovery</b>
              <p><small>Tell Fuzzie about your API schema in one of the following ways</small></p>
              <v-divider />

                <div class="mb-2">
                  <label for="rq-text" class="form-label">Request Text</label>
                  <textarea class="form-control" id="rq-text" rows="4" v-model="newContext.requestTextContent"></textarea>
                </div>

                <div class="mb-2">
                  <label for="rt-file" class="form-label">Request Text File</label>
                  <input class="form-control form-control-sm" type="file" id="rt-file" ref="rtFileInput" @change="onRequestTextFileChange">
                </div>

                <div class="mb-2 mt-3">
                  <label for="openapi3-file" class="form-label">OpenAPI 3 / Swagger File</label>
                  <input class="form-control form-control-sm" type="file" id="openapi3-file" ref="openapi3FileInput" @change="onOpenApi3FileChange">
                </div>

                <div class="mt-3">
                  <label for="openapi3-url" class="form-label">OpenAPI 3 / Swagger URL</label>
                  <input class="form-control form-control-sm" type="text" id="openapi3-url" v-model="newContext.openapi3Url">
                </div>
              </form>
            </div>
            <div class="col-6">
              
              <form>

                <b>API Authentication</b>
                <v-divider />

                <div class="btn-group btn-group-sm" role="group" aria-label="Basic radio toggle button group">
                  <input type="radio" class="btn-check" name="btnradio" id="authn-noauthn" autocomplete="off" >
                  <label class="btn btn-outline-warning" for="authn-noauthn" @click="(
                    newContext.isanonymous = true,
                    securityBtnVisibility.basic=false,
                    securityBtnVisibility.bearer=false,
                    securityBtnVisibility.apikey=false
                  )">No Authentication</label>

                  <input type="radio" class="btn-check" name="btnradio" id="authn-basic" value="0" autocomplete="off">
                  <label class="btn btn-outline-success" for="authn-basic" @click="(
                    newContext.isanonymous = false,
                    securityBtnVisibility.basic=true,
                    securityBtnVisibility.bearer=false,
                    securityBtnVisibility.apikey=false
                  )">Basic Username/Password</label>

                  <input type="radio" class="btn-check" name="btnradio" id="authn-bearer" autocomplete="off">
                  <label class="btn btn-outline-success" for="authn-bearer" @click="(
                    newContext.isanonymous = false,
                    securityBtnVisibility.basic=false,
                    securityBtnVisibility.bearer=true,
                    securityBtnVisibility.apikey=false
                  )">Bearer Token</label>

                  <input type="radio" class="btn-check" name="btnradio" id="authn-apikey" autocomplete="off">
                  <label class="btn btn-outline-success" for="authn-apikey" @click="(
                    newContext.isanonymous = false,
                    securityBtnVisibility.basic=false,
                    securityBtnVisibility.bearer=false,
                    securityBtnVisibility.apikey=true
                  )">API Key</label>
                </div>

                <v-divider />

                <div class="form-group mb-3" v-show="securityBtnVisibility.basic">
                  <label for="username">Username</label>
                  <input type="text" class="form-control form-control-sm" id="username"  placeholder="username">
                </div>
                <div class="form-group  mb-3" v-show="securityBtnVisibility.basic">
                  <label for="password">Password</label>
                  <v-text-field
                    v-model="password"
                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="show1 ? 'text' : 'password'"
                    name="password"
                    counter
                    @click:append="show1 = !show1"
                  ></v-text-field>
                  <!-- <input type="password" class="form-control form-control-sm" id="username"  placeholder="password"> -->
                </div>

                <div class="form-group mb-3" v-show="securityBtnVisibility.bearer">
                  <label for="header">Header</label>
                  <input type="text" class="form-control form-control-sm" id="header" value="Authorization">
                </div>
                <div class="form-group mb-3" v-show="securityBtnVisibility.bearer">
                  <label for="header">Token</label>
                  <input type="text" class="form-control form-control-sm" id="header">
                </div>

                <div class="form-group mb-3" v-show="securityBtnVisibility.apikey">
                  <label for="apikeyheader">API Key Header</label>
                  <input type="text" class="form-control form-control-sm" id="apikeyheader" value="Authorization">
                </div>
                <div class="form-group mb-3" v-show="securityBtnVisibility.apikey">
                  <label for="apikey">Key</label>
                  <input type="text" class="form-control form-control-sm" id="apikey">
                </div>

                <v-divider />

                <b>Fuzz Properties</b>
                <v-divider />
                <v-divider />
                
                <v-slider
                  v-model="newContext.fuzzcaseToExec"
                  label=''
                  track-color="blue"
                  thumb-color="red"
                  thumb-label="always"
                  min=100
                  max=50000
                  step="10"
                ></v-slider>

              </form>
              
              <v-divider />

              <div style="text-align:right">
                <button class="btn btn-warning mr-3" @click="clearContextForm">Reset</button>
                <button class="btn btn-primary" @click="createNewContext">Create</button>
              </div>
            <!-- col end-->
            </div>
        </div>
      </div>
    </Sidebar>

    <v-card
    color="white"
    outlined
    width="100%"
    height="100%">
      <v-toolbar card color="cyan" flat dense height="50px">
        <v-spacer />
        <v-btn  variant="plain" height="30px" v-bind="attrs" v-on="on" size="small" @click="newContextSideBarVisible = true">
              New Context
        </v-btn>
      </v-toolbar>
      <div heigh="100%">
          <Tree :value="nodes" selectionMode="single" v-show="showTree">
              <template #default="slotProps">
                <div v-on:click="onFuzzContextSelected(slotProps.node.key)">
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
        </div>
    </v-card>
  </div>
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
import { HtmlHTMLAttributes } from '@vue/runtime-dom';

declare var vscode: any;

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
  isFuzzcontextsGetComplete = true;
  nodes: TreeNode[] = [];
  showTree = this.nodes.length > 0 ? "true": "false";
  newContextSideBarVisible = false;
  toast = useToast();

  securityBtnVisibility= {
    anonymous: false,
    basic: false,
    bearer: false,
    apikey: false

  }

  newContext= {
    apiDiscoveryMethod: 'openapi3',
    isanonymous: true,
    name: '',
    requestTextContent: '',
    requestTextFilePath: '',
    openapi3FilePath: '',
    openapi3Url: '',
    openapi3Content: '',
    basicUsername: '', 
    basicPassword: '', 
    bearerTokenHeader: '', 
    bearerToken: '', 
    apikeyHeader: '', 
    apikey: '', 
    hostname: '',
    port: 443,
    fuzzcaseToExec: 100,
    authnType: ''
  } 
  
  mounted() {
    this.getFuzzcontexts()

    this.vscodeMsger.subscribe("file-content-result", this.readFileContentResult);
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
      this.isFuzzcontextsGetComplete = false;
      const fcs = await this.fm.getFuzzcontexts()    

      if (fcs.length > 0)
      {
        this.nodes = this.createTreeNodesFromFuzzcontexts(fcs);
      }

      this.isFuzzcontextsGetComplete = true;
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
      this.newContext.requestTextContent = content;
    }
    else
    {
      this.clearRequestTextFileInput();
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
      this.newContext.openapi3Content = content;
    }
    else
    {
      this.clearOpenApiFileInput();
      this.toast.add({severity:'error', summary: 'Invalid File Type', detail:'OpenAPI3 spec files are yaml or json', life: 5000});
    }
  }

  createNewContext() {
    
    this.newContext.authnType = this.determineAuthnType();
    this.newContext.apiDiscoveryMethod = this.determineApiDiscoveryMethod();

  }

  // Anonymous = "Anonymous",
  // Basic = "Basic",
  // Bearer = "Bearer",
  // ApiKey = "ApiKey"
  determineAuthnType(): string {

    if(this.newContext.isanonymous)
    {
      return "Anonymous";
    }
    else if(this.newContext.basicUsername != '' && this.newContext.basicPassword != '')
    {
       return "Basic";
    }
    else if(this.newContext.apikeyHeader != '' && this.newContext.apikey != '')
    {
       return  "ApiKey";
    }
    else if(this.newContext.bearerToken != '')
    {
       return  "Bearer";
    }

    return "Anonymous";
  }

  determineApiDiscoveryMethod(){
    if(this.newContext.requestTextContent != '')
    {
        return 'openapi3';
    }
    return 'request-text';
  }

  clearContextForm() {

    
    this.clearOpenApiFileInput();
    this.clearRequestTextFileInput();
    
    this.newContext = {
        apiDiscoveryMethod: '',
        isanonymous: false,
        name: '',
        requestTextContent: '',
        requestTextFilePath: '',
        openapi3FilePath: '',
        openapi3Url: '',
        openapi3Content: '',
        basicUsername: '', 
        basicPassword: '', 
        bearerTokenHeader: '', 
        bearerToken: '', 
        apikeyHeader: '', 
        apikey: '', 
        hostname: '',
        port: 443,
        fuzzcaseToExec: 100,
        authnType: 'Anonymous'
    };
  }

  clearOpenApiFileInput()
  {
    const openapi3Unknown = this.$refs["openapi3FileInput"] as unknown;
    const openapiEle = openapi3Unknown as HTMLInputElement;
    openapiEle.value = '';
  }

  clearRequestTextFileInput()
  {
    const rtUnknown = this.$refs["rtFileInput"] as unknown;
    const rtEle = rtUnknown as HTMLInputElement;
    rtEle.value = '';
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
