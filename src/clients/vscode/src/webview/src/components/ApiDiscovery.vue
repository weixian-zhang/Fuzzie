<!-- https://pictogrammers.github.io/@mdi/font/6.9.96/ -->

<template>
  <div>
    <!-- new context -->
    <Sidebar v-model:visible="newContextSideBarVisible" position="right" style="width:950px;">
      
      <div class="container-fluid">
        <div class="row">
            <div class="col-6">
              <form>
                <div class="form-group">
                  <label for="contextName">Name</label>
                  <input type="text" class="form-control form-control-sm" id="contextName"  placeholder="fuzz context name" v-model="newContext.name">
                </div>

              <v-divider />
              <b>Test Properties</b>
              <v-divider />

              <div class="form-group mb-3" >
                  <label for="hostname">Hostname</label>
                  <input type="text" class="form-control form-control-sm" id="hostname"  placeholder="hostname" v-model="newContext.hostname">
                </div>

                <div class="form-group">
                  <label for="port">Port</label>
                  <input type="text" class="form-control form-control-sm" id="port"  placeholder="port" v-model="newContext.port">
                </div>

              <v-divider />
              <b>API Discovery</b>
              <v-divider />

              <small>Tell Fuzzie about your API schema in one of the following ways</small>

                <div class="mb-2">
                  <label for="rq-text" class="form-label">Request Text</label>
                  <textarea class="form-control" id="rq-text" rows="4" v-model="newContext.requestText"></textarea>
                </div>

                <div class="mb-2">
                  <label for="openapi3-file" class="form-label">Request Text File</label>
                  <input class="form-control form-control-sm" type="file" id="openapi3-file" >
                </div>

                <div class="mb-2 mt-3">
                  <label for="openapi3-file" class="form-label">OpenAPI 3 / Swagger File</label>
                  <input class="form-control form-control-sm" type="file" id="openapi3-file">
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
                  <label for="username">Password</label>
                  <input type="password" class="form-control form-control-sm" id="username"  placeholder="password">
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
              </form>

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
import Tree, { TreeNode } from 'primevue/tree';
import dateformat from 'dateformat';
import Sidebar from 'primevue/sidebar';
import VSCodeMessager from '../services/VSCodeMessager';

declare var vscode: any;

class Props {
  // optional prop
  eventemitter: any = {}
  vscodeMsger: VSCodeMessager;
}

@Options({
  components: {
    Tree,
    Sidebar
  }
})



export default class ApiDiscovery extends Vue.with(Props) {
  
  fm = new FuzzerManager();
  isFuzzcontextsGetComplete = true;
  nodes: TreeNode[] = [];
  showTree = this.nodes.length > 0 ? "true": "false";
  newContextSideBarVisible = false;
  
  securityBtnVisibility= {
    anonymous: false,
    basic: false,
    bearer: false,
    apikey: false

  }

  newContext= {
    isanonymous: false,
    name: '',
    requestText: '',
    requestTextFilePath: '',
    openapi3FilePath: '',
    openapi3Url: '',
    basicUsername: '', 
    basicPassword: '', 
    bearerTokenHeader: '', 
    bearerToken: '', 
    apikeyHeader: '', 
    apikey: '', 
    hostname: '',
    port: 443,
    fuzzMode: '',
    fuzzcaseToExec: 100,
    authnType: ''
  } 
  
  mounted() {
    this.getFuzzcontexts()
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

  showNewContextSideBar() {
      return;
  }

  createNewContext() {
    
    if(this.newContext.openapi3FilePath != '')
    {
      this.vscodeMsger.send('read-file-content', this.newContext.openapi3FilePath);
    }
  }

  clearContextForm() {
    this.newContext = {
        isanonymous: false,
        name: '',
        requestText: '',
        requestTextFilePath: '',
        openapi3FilePath: '',
        openapi3Url: '',
        basicUsername: '', 
        basicPassword: '', 
        bearerTokenHeader: '', 
        bearerToken: '', 
        apikeyHeader: '', 
        apikey: '', 
        hostname: '',
        port: 443,
        fuzzMode: '',
        fuzzcaseToExec: 100,
        authnType: ''
    };
  }

  // newContextObject() {

  //   this.newContext = {
  //     isanonymous: false,
  //     name: '',
  //     requestText: '',
  //     requestTextFilePath: '',
  //     openapi3FilePath: '',
  //     openapi3Url: '',
  //     basicUsername: '', 
  //     basicPassword: '', 
  //     bearerTokenHeader: '', 
  //     bearerToken: '', 
  //     apikeyHeader: '', 
  //     apikey: '', 
  //     hostname: '',
  //     port: 443,
  //     fuzzMode: '',
  //     fuzzcaseToExec: 100,
  //     authnType: ''
  //   } 

    
    
  // }

}
</script>


<style scoped>
input[type=text]{
   padding:0px;
   margin-bottom:2px; /* Reduced from whatever it currently is */
   margin-top:2px; /* Reduced from whatever it currently is */
}
</style>
