<!-- https://pictogrammers.github.io/@mdi/font/6.9.96/ -->

<template>

    <!--v-card height affects Splitter in Master height="455px" -->
    <v-card
    color="white"
    outlined >

     <!-- new context -->
     <Sidebar v-model:visible="newContextSideBarVisible" position="right" style="width:950px;">
      
      <div class="container-fluid">
        <div class="row mb-3"><h5>Create new Fuzz Context</h5></div>
        <div class="row">
            <div class="col-6">
              <form>
                <div class="form-group">
                  <v-text-field
                    v-model="newApiContext.name"
                    variant="underlined"
                    :rules="[() => !!newApiContext.hostname || 'This field is required']"
                    counter="40"
                    density="compact"
                    hint="e.g: my REST/GraphQL API"
                    label="Name"
                    clearable
                  ></v-text-field>
                </div>

              <v-divider />
              <b>Test Properties</b>
              <v-divider />

              <div class="form-group mb-3" >
                <v-text-field
                    v-model="newApiContext.hostname"
                    variant="underlined"
                    :rules="[() => !!newApiContext.hostname || 'This field is required']"
                    density="compact"
                    hint=""
                    label="Hostname" 
                    clearable/>
                </div>

                <div class="form-group">
                  <v-text-field
                    v-model="newApiContext.port"
                    type="number" 
                    variant="underlined"
                    :rules="[() => !!newApiContext.port || 'This field is required']"
                    density="compact"
                    hint=""
                    max="65535"
                    label="Port number" />
                </div>

              <v-divider />
              <b>API Discovery</b>
              <p><small>Tell Fuzzie about your API schema in one of the following ways</small></p>
              <v-divider />

                <div class="mb-2">
                  <v-textarea 
                    label="Request Text" 
                    variant="underlined" 
                    v-model="newApiContext.requestTextContent"
                     density="compact"
                     clearable
                     @click:clear="(newApiContext.requestTextContent='')"
                  ></v-textarea>
                </div>

                <div class="mb-2">
                  <v-file-input
                    v-model="requestTextFileInputFileVModel"
                    label="Request Text File"
                    density="compact"
                    ref="rtFileInput"
                    @change="onRequestTextFileChange"
                    variant="underlined"
                    clearable
                    @click:clear="(
                      requestTextFileInputFileVModel=[],
                      newApiContext.requestTextContent='',
                      newApiContext.requestTextFilePath=''
                    )"
                  ></v-file-input>
                </div>

                <div class="mb-2 mt-3">
                  <v-file-input
                    label="OpenAPI 3 File"
                    v-model="openapi3FileInputFileVModel"
                    density="compact"
                    @change="onOpenApi3FileChange"
                    ref="openapi3FileInput" 
                    clearable
                    @click:clear="(
                      openapi3FileInputFileVModel=[],
                      newApiContext.openapi3Content='',
                      newApiContext.openapi3FilePath=''
                    )"
                    variant="underlined"
                  ></v-file-input>
                </div>

                <div class="mt-3">
                  <v-text-field
                    v-model="newApiContext.openapi3Url"
                    variant="underlined"
                    hint="e.g: https://openapi3/spec/yaml"
                    :rules="inputRules"
                    density="compact"
                    clearable
                    @click:clear="(
                      newApiContext.openapi3Url=''
                    )"
                    label="OpenAPI 3 URL" />
                </div>
              </form>
            </div>
            <div class="col-6">
              
              <form>

                <b>API Authentication</b>
                <v-divider />

                <div class="btn-group btn-group-sm" role="group" aria-label="Basic radio toggle button group">

                  <input type="radio" class="btn-check" name="btnradio" id="authn-noauthn" :checked="securityBtnVisibility.anonymous == true">
                  <label class="btn btn-outline-warning small" for="authn-noauthn" @click="(
                    newApiContext.authnType='Anonymous',
                    securityBtnVisibility.anonymous = true,
                    securityBtnVisibility.basic=false,
                    securityBtnVisibility.bearer=false,
                    securityBtnVisibility.apikey=false
                  )">No Authentication</label>

                  <input type="radio" class="btn-check" name="btnradio" id="authn-basic" :checked="securityBtnVisibility.basic == true">
                  <label class="btn btn-outline-success small" for="authn-basic" @click="(
                    newApiContext.authnType='Basic',
                    securityBtnVisibility.anonymous=false,
                    securityBtnVisibility.basic=true,
                    securityBtnVisibility.bearer=false,
                    securityBtnVisibility.apikey=false
                  )">Basic Username/Password</label>

                  <input type="radio" class="btn-check" name="btnradio" id="authn-bearer" :checked="securityBtnVisibility.bearer == true">
                  <label class="btn btn-outline-success small" for="authn-bearer" @click="(
                    newApiContext.authnType='Bearer',
                    securityBtnVisibility.anonymous =false,
                    securityBtnVisibility.basic=false,
                    securityBtnVisibility.bearer=true,
                    securityBtnVisibility.apikey=false
                  )">Bearer Token</label>

                  <input type="radio" class="btn-check" name="btnradio" id="authn-apikey" :checked="securityBtnVisibility.apikey == true">
                  <label class="btn btn-outline-success small" for="authn-apikey" @click="(
                    newApiContext.authnType='ApiKey',
                    securityBtnVisibility.anonymous=false,
                    securityBtnVisibility.basic=false,
                    securityBtnVisibility.bearer=false,
                    securityBtnVisibility.apikey=true
                  )">API Key</label>
                </div>

                <v-divider />

                <!-- column 2 security -->
                <div class="form-group mb-3" v-show="securityBtnVisibility.basic">
                  <v-text-field
                    v-model="newApiContext.basicUsername"
                    variant="underlined"
                    hint=""
                    density="compact"
                    label="Username" 
                    clearable
                    @click:clear="(newApiContext.basicUsername='')"
                    />
                </div>
                <div class="form-group  mb-3" v-show="securityBtnVisibility.basic">
                  <v-text-field
                    v-model="newApiContext.basicPassword"
                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPasswordValue ? 'text' : 'password'"
                    name="password"
                    label="Password"
                    density="compact"
                    variant="underlined"
                    counter
                    clearable
                    @click:clear="(newApiContext.basicPassword='')"
                    @click:append="showPasswordValue= !showPasswordValue"
                  ></v-text-field>

                </div>

                <div class="form-group mb-3" v-show="securityBtnVisibility.bearer">
                  <v-text-field
                    v-model="newApiContext.bearerTokenHeader"
                    variant="underlined"
                    counter="25"
                    hint="default Authorization"
                    density="compact"
                    label="HTTP Header"
                    clearable
                    @click:clear="(newApiContext.bearerTokenHeader='')"
                  ></v-text-field>
                </div>
                <div class="form-group mb-3" v-show="securityBtnVisibility.bearer">
                  <v-text-field
                    v-model="newApiContext.bearerToken"
                    variant="underlined"
                    counter="25"
                    hint="bearer token"
                    label="Token"
                    density="compact"
                    clearable
                    @click:clear="(newApiContext.bearerToken='')"
                  ></v-text-field>
                </div>

                <div class="form-group mb-3" v-show="securityBtnVisibility.apikey">
                  <v-text-field
                    v-model="newApiContext.apikeyHeader"
                    variant="underlined"
                    counter="25"
                    hint="default Authorization"
                    label="HTTP Header"
                    density="compact"
                    clearable
                     @click:clear="(newApiContext.apikeyHeader='')"
                  ></v-text-field>
                </div>
                <div class="form-group mb-3" v-show="securityBtnVisibility.apikey">
                  <v-text-field
                    v-model="newApiContext.apikey"
                    variant="underlined"
                    counter="25"
                    hint="API Key"
                    label="API Key"
                    density="compact"
                    clearable
                     @click:clear="(newApiContext.apikey='')"
                  ></v-text-field>
                </div>

                <v-divider />

                <b>Fuzz Properties</b>
                <v-divider />
                <v-divider />
                
                <v-slider
                  v-model="newApiContext.fuzzcaseToExec"
                  label=''
                  track-color="blue"
                  thumb-color="red"
                  thumb-label="always"
                  min=100
                  max=50000
                  step="5"
                ></v-slider>

              </form>
              
              <v-divider />

              <div style="text-align:right">
                <button class="btn btn-warning mr-3" @click="clearContextForm">Reset</button>
                <button class="btn btn-primary" @click="createNewApiContext">Create</button>
              </div>
            <!-- col end-->
            </div>
        </div>
      </div>
    </Sidebar>

    <!--update context-->
    <!-- new context -->
     <Sidebar v-model:visible="updateContextSideBarVisible" position="right" style="width:950px;">
      
      <div class="container-fluid">
        <div class="row mb-3"><h5>Create new Fuzz Context</h5></div>
        <div class="row">
            <div class="col-6">
              <form>
                <div class="form-group">
                  <v-text-field
                    v-model="apiContextEdit.name"
                    variant="underlined"
                    :rules="[() => !!apiContextEdit.hostname || 'This field is required']"
                    counter="25"
                    density="compact"
                    hint="e.g: my REST/GraphQL API"
                    label="Name"
                    clearable
                  ></v-text-field>
                </div>

              <v-divider />
              <b>Test Properties</b>
              <v-divider />

              <div class="form-group mb-3" >
                <v-text-field
                    v-model="newApiContext.hostname"
                    variant="underlined"
                    :rules="[() => !!apiContextEdit.hostname || 'This field is required']"
                    density="compact"
                    hint=""
                    label="Hostname" 
                    clearable/>
                </div>

                <div class="form-group">
                  <v-text-field
                    v-model="apiContextEdit.port"
                    type="number" 
                    variant="underlined"
                    :rules="[() => !!apiContextEdit.port || 'This field is required']"
                    density="compact"
                    hint=""
                    max="65535"
                    label="Port number" />
                </div>

              <v-divider />
              <b>API Discovery (Read-Only)</b>
              <p><small>Tell Fuzzie about your API schema in one of the following ways</small></p>
              <v-divider />

                <div class="mb-2">
                  <v-textarea 
                    label="Request Text" 
                    variant="underlined" 
                    v-model="apiContextEdit.requestTextContent"
                     density="compact"
                     readonly
                  ></v-textarea>
                </div>

                <div class="mb-2">
                  <v-text-field
                    v-model="apiContextEdit.requestTextFilePath"
                    variant="underlined"
                    density="compact"
                    readonly
                    label="Request Text File Path" />
                </div>

                <div class="form-group">
                  <v-text-field
                    v-model="apiContextEdit.openapi3FilePath"
                    variant="underlined"
                    density="compact"
                    readonly
                    label="OpenAPI 3 File Path" />
                </div>

                <div class="form-group">
                  <v-text-field
                    v-model="apiContextEdit.openapi3Url"
                    variant="underlined"
                    density="compact"
                    readonly
                    label="Request Text File Path" />
                </div>
              </form>
            </div>
            <div class="col-6">
              
              <form>

                <b>API Authentication</b>
                <v-divider />

                <div class="btn-group btn-group-sm" role="group" aria-label="Basic radio toggle button group">

                  <input type="radio" class="btn-check" name="btnradio" id="authn-noauthn" :checked="securityBtnVisibility.anonymous == true">
                  <label class="btn btn-outline-warning small" for="authn-noauthn" @click="(
                    newApiContext.authnType='Anonymous',
                    securityBtnVisibility.anonymous = true,
                    securityBtnVisibility.basic=false,
                    securityBtnVisibility.bearer=false,
                    securityBtnVisibility.apikey=false
                  )">No Authentication</label>

                  <input type="radio" class="btn-check" name="btnradio" id="authn-basic" :checked="securityBtnVisibility.basic == true">
                  <label class="btn btn-outline-success small" for="authn-basic" @click="(
                    newApiContext.authnType='Basic',
                    securityBtnVisibility.anonymous=false,
                    securityBtnVisibility.basic=true,
                    securityBtnVisibility.bearer=false,
                    securityBtnVisibility.apikey=false
                  )">Basic Username/Password</label>

                  <input type="radio" class="btn-check" name="btnradio" id="authn-bearer" :checked="securityBtnVisibility.bearer == true">
                  <label class="btn btn-outline-success small" for="authn-bearer" @click="(
                    newApiContext.authnType='Bearer',
                    securityBtnVisibility.anonymous =false,
                    securityBtnVisibility.basic=false,
                    securityBtnVisibility.bearer=true,
                    securityBtnVisibility.apikey=false
                  )">Bearer Token</label>

                  <input type="radio" class="btn-check" name="btnradio" id="authn-apikey" :checked="securityBtnVisibility.apikey == true">
                  <label class="btn btn-outline-success small" for="authn-apikey" @click="(
                    newApiContext.authnType='ApiKey',
                    securityBtnVisibility.anonymous=false,
                    securityBtnVisibility.basic=false,
                    securityBtnVisibility.bearer=false,
                    securityBtnVisibility.apikey=true
                  )">API Key</label>
                </div>

                <v-divider />

                <!-- column 2 security -->
                <div class="form-group mb-3" v-show="securityBtnVisibility.basic">
                  <v-text-field
                    v-model="apiContextEdit.basicUsername"
                    variant="underlined"
                    hint=""
                    density="compact"
                    label="Username" 
                    clearable
                    @click:clear="(apiContextEdit.basicUsername='')"
                    />
                </div>
                <div class="form-group  mb-3" v-show="securityBtnVisibility.basic">
                  <v-text-field
                    v-model="apiContextEdit.basicPassword"
                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPasswordValue ? 'text' : 'password'"
                    name="password"
                    label="Password"
                    density="compact"
                    variant="underlined"
                    counter
                    clearable
                    @click:clear="(apiContextEdit.basicPassword='')"
                    @click:append="showPasswordValue= !showPasswordValue"
                  ></v-text-field>

                </div>

                <div class="form-group mb-3" v-show="securityBtnVisibility.bearer">
                  <v-text-field
                    v-model="apiContextEdit.bearerTokenHeader"
                    variant="underlined"
                    counter="25"
                    hint="default Authorization"
                    density="compact"
                    label="HTTP Header"
                    clearable
                    @click:clear="(apiContextEdit.bearerTokenHeader='')"
                  ></v-text-field>
                </div>
                <div class="form-group mb-3" v-show="securityBtnVisibility.bearer">
                  <v-text-field
                    v-model="apiContextEdit.bearerToken"
                    variant="underlined"
                    counter="25"
                    hint="bearer token"
                    label="Token"
                    density="compact"
                    clearable
                    @click:clear="(apiContextEdit.bearerToken='')"
                  ></v-text-field>
                </div>

                <div class="form-group mb-3" v-show="securityBtnVisibility.apikey">
                  <v-text-field
                    v-model="apiContextEdit.apikeyHeader"
                    variant="underlined"
                    counter="25"
                    hint="default Authorization"
                    label="HTTP Header"
                    density="compact"
                    clearable
                     @click:clear="(apiContextEdit.apikeyHeader='')"
                  ></v-text-field>
                </div>
                <div class="form-group mb-3" v-show="securityBtnVisibility.apikey">
                  <v-text-field
                    v-model="apiContextEdit.apikey"
                    variant="underlined"
                    counter="25"
                    hint="API Key"
                    label="API Key"
                    density="compact"
                    clearable
                     @click:clear="(apiContextEdit.apikey='')"
                  ></v-text-field>
                </div>

                <v-divider />

                <b>Fuzz Properties</b>
                <v-divider />
                <v-divider />
                
                <v-slider
                  v-model="apiContextEdit.fuzzcaseToExec"
                  label=''
                  track-color="blue"
                  thumb-color="red"
                  thumb-label="always"
                  min=100
                  max=50000
                  step="5"
                ></v-slider>

              </form>
              
              <v-divider />

              <div style="text-align:right">
                <button class="btn btn-primary" @click="updateApiContext">Update</button>
              </div>
            <!-- col end-->
            </div>
        </div>
      </div>
    </Sidebar>

    <!-- delete confirmation -->
    <v-dialog
      v-model="showDeleteConfirmDialog"
      width="400"
    >
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Delete API Fuzz Context
        </v-card-title>

        <v-card-text>
          Delete {{apiContextToDelete.name}}?
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <button class="btn btn-primary mr-3" @click="showDeleteConfirmDialog = false">Cancel</button>
          <button class="btn btn-danger" @click="deleteApiFuzzContext">Delete</button>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-toolbar card color="cyan" flat dense height="50px">

      <v-toolbar-title>Fuzz Contexts</v-toolbar-title>

      <v-btn  variant="plain" height="30px" plain icon v-tooltip.bottom="'create new messaging fuzz context (in roadmap)'">
        <v-icon>mdi-message-plus-outline</v-icon>
      </v-btn>

      <v-btn color="accent" variant="plain" height="30px" plain icon v-tooltip.right="'refresh fuzz contexts'"
      :disabled="!isGetFuzzContextFinish"
        @click="getFuzzcontexts">
            <v-icon>mdi-refresh</v-icon>
      </v-btn>

      <v-btn v-tooltip.bottom="'create new API fuzz context'" icon  variant="plain" height="30px" plain  @click="newContextSideBarVisible = true">
        <v-icon>mdi-api</v-icon>
      </v-btn>

    </v-toolbar>
    <div maximizable
            class="p-fluid">
            <Tree :value="nodes" selectionMode="single" :expandedKeys="{'-1':true, '-2':true}" v-show="showTree" scrollHeight="300px" width="100%"  >
          <template #default="slotProps">
            <small><b v-on:click="onFuzzContextSelected(slotProps.node.fuzzcontextId)">{{slotProps.node.label}}</b></small>
                <span v-if="slotProps.node.key != '-1' && slotProps.node.key != '-2'">
                    <v-spaces />
                    [<v-icon
                      variant="flat"
                      icon="mdi-pencil"
                      color="primary"
                      size="x-small"
                      @click="(
                        onEditFuzzContextClicked(slotProps.node.data)
                      )"
                      ></v-icon>]
                      [<v-icon
                      variant="flat"
                      icon="mdi-delete"
                      color="primary"
                      size="x-small"
                      @click="(
                        onDeleteFuzzContextClicked(slotProps.node.data)
                      )"
                      ></v-icon>]
                  </span>
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
</template>

<script lang="ts">

import { Options, Vue } from 'vue-class-component';
import { useToast } from "primevue/usetoast";
import Tree, { TreeNode } from 'primevue/tree';
import dateformat from 'dateformat';
import Sidebar from 'primevue/sidebar';
import VSCodeMessager, {Message} from '../services/VSCodeMessager';
import Utils from '../Utils';
import { ApiFuzzContext, ApiFuzzContextUpdate } from '../Model';
import FuzzerWebClient from "../services/FuzzerWebClient";
import FuzzerManager from "../services/FuzzerManager";

class Props {
  // optional prop
  eventemitter: any = {}
  vscodeMsger: VSCodeMessager;
  fuzzermanager: FuzzerManager
  webclient : FuzzerWebClient
}

@Options({
  components: {
    Tree,
    Sidebar
  },
})


export default class ApiDiscovery extends Vue.with(Props) {
  
  
  openapi3FileInputFileVModel: Array<any> = [];
  requestTextFileInputFileVModel: Array<any>  = [];
  showPasswordValue = false;
  nodes: TreeNode[] = [];
  showTree = this.nodes.length > 0 ? "true": "false";
  showDeleteConfirmDialog = false;
  newContextSideBarVisible = false;
  updateContextSideBarVisible = false;
  isGetFuzzContextFinish = true;
  apiContextToDelete: any = {};
  toast = useToast();

  inputRules= [
        () => !!Utils.isValidHttpUrl(this.newApiContext.openapi3Url) || "URL is not valid"
  ];

  securityBtnVisibility = {
    anonymous: true,
    basic: false,
    bearer: false,
    apikey: false

  }

  newApiContext= new ApiFuzzContext();
  apiContextEdit = new ApiFuzzContext();

  //methods
  
  mounted() {
    this.getFuzzcontexts()
  }

  onEditFuzzContextClicked(data) {
    this.apiContextEdit = data;
    this.updateContextSideBarVisible = true;
  }

  onDeleteFuzzContextClicked(data) {
    this.apiContextToDelete = {
                          Id: data.Id,
                          name: data.name,
                        },
    this.showDeleteConfirmDialog = true
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
      const [OK, err, fcs] = await this.fuzzermanager.getFuzzcontexts()    

      if (OK)
      {
        this.nodes = [];
        this.nodes = this.createTreeNodesFromFuzzcontexts(fcs);
      }
      else
      {
        this.toast.add({severity:'error', summary: '', detail:err, life: 5000});
      }

      this.isGetFuzzContextFinish = true;

    } catch (error) {
        //TODO: log
        console.log(error)
    }
  }

  createTreeNodesFromFuzzcontexts(fcs: ApiFuzzContext[]): TreeNode[] {

    const nodes: TreeNode[] = [];

    const apiNode = {
        key: "-1",
        label: "API",
        children: new Array<any>()
      };
    const msgApi = {
        key: "-2",
        label: "Messaging",
        children: new Array<any>()
      };

    nodes.push(apiNode);
    nodes.push(msgApi);

    fcs.forEach(fc => {

        if(fc instanceof ApiFuzzContext)
        {
            const fcNode: any = {
              key: fc.Id,
              fuzzcontextId: fc.Id,
              label: fc.name,
              data: fc
            };

            apiNode.children.push(fcNode);

            fc.fuzzCaseSetRuns.forEach(fcsr => {

            const casesetNode = {
              key: fcsr.fuzzCaseSetRunsId,
              fuzzcontextId: fcsr.fuzzcontextId,
              fuzzCaseSetRunsId: fcsr.fuzzCaseSetRunsId,
              isFuzzing: false,
              label: dateformat(fcsr.startTime, "ddd, mmm dS, yy - h:MM:ss TT"), //`${nodeLabel.toLocaleDateString('en-us')} ${nodeLabel.toLocaleTimeString()}`,
              data: fcsr
            };
          
            if(fcNode.children == undefined)
            {
              fcNode.children = [];
            }

            fcNode.children.push(casesetNode);

          });

        }
    });

    return nodes;

  }

  onFuzzContextSelected(fuzzcontextId) {
    this.eventemitter.emit("onFuzzContextSelected", fuzzcontextId);
  }

  async onRequestTextFileChange(event) {
    console.log(event);

    const files = event.target.files;

    const file = files[0];

    const reader = new FileReader();
    if (file.name.includes(".http") || file.name.includes(".fuzzie") || file.name.includes(".text")) {

      const content = await Utils.readFileAsText(file);
      this.newApiContext.requestTextContent = content;

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
      this.newApiContext.openapi3Content = content;

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

  async deleteApiFuzzContext() {
      const id = this.apiContextToDelete.Id;
      const [ok, error] = await this.fuzzermanager.deleteApiFuzzContext(id);

    if(!ok)
    {
      this.toast.add({severity:'error', summary: 'Delete API FuzzContext', detail:error, life: 5000});
    }
    else
    {
      this.eventemitter.emit("onFuzzContextDelete", id);
      this.getFuzzcontexts();
      this.toast.add({severity:'success', summary: 'Delete API FuzzContext', detail:`${this.apiContextToDelete.name} updated successfully`, life: 5000});
    }

    this.showDeleteConfirmDialog = false;
    this.apiContextToDelete = {};
  }

  async updateApiContext() {
    const apiFCUpdate = new ApiFuzzContextUpdate();
    
    apiFCUpdate.fuzzcontextId = this.apiContextEdit.Id;

    Utils.mapProp(this.apiContextEdit, apiFCUpdate);

    const [ok, error] = await this.fuzzermanager.updateApiFuzzContext(apiFCUpdate);

    if(!ok)
    {
      this.toast.add({severity:'error', summary: 'Update API FuzzContext', detail:error, life: 5000});
    }
    else
    {
      this.apiContextEdit = new ApiFuzzContext();
      this.toast.add({severity:'success', summary: 'Update API FuzzContext', detail:`${apiFCUpdate.name} updated successfully`, life: 5000});
    }

    this.updateContextSideBarVisible = false;
  }

  async createNewApiContext() {
    
    this.newApiContext.authnType = this.determineAuthnType();

    this.newApiContext.apiDiscoveryMethod = this.determineApiDiscoveryMethod();

    if(this.newApiContext.name == '' || this.newApiContext.hostname == '' || this.newApiContext.port == undefined)
    {
      this.toast.add({severity:'error', summary: 'Missing Info', detail:'Name, hostname, port are required', life: 5000});
      return;
    }

    if(this.newApiContext.openapi3Url != '') {
      const [ok, error, data] = await this.fuzzermanager.httpGetOpenApi3FromUrl(this.newApiContext.openapi3Url)

      if(!ok)
      {
        this.toast.add({severity:'error', summary: 'Trying to get OpenApi3 spec by Url', detail:error, life: 5000});
        return;
      }

      this.newApiContext.openapi3Content = data;

    }

    if(this.newApiContext.openapi3Content == '' && this.newApiContext.requestTextContent == '')
    {
      this.toast.add({severity:'error', summary: 'API Discovery', detail:'need either OpenAPI 3 spec or Request Text to create context', life: 5000});
      return;
    }

   
    const apifc: ApiFuzzContext = Utils.copy(this.newApiContext);
    apifc.openapi3Content = apifc.openapi3Content != '' ? btoa(apifc.openapi3Content) : '';
    apifc.requestTextContent = apifc.requestTextContent != '' ? btoa(apifc.requestTextContent) : '';

    const result =  await this.fuzzermanager.newFuzzContext(apifc);
    const ok = result['ok'];
    const error =result['error'];

    if(!ok && error != '')
    {
      this.toast.add({severity:'error', summary: 'Create new API context', detail:error, life: 5000});
      return;
    }
    else
    {
      this.newContextSideBarVisible = false;
      this.getFuzzcontexts();
      this.toast.add({severity:'success', summary: 'API Fuzz Context created', detail:error, life: 3000});

      //reset form
      this.openapi3FileInputFileVModel = [];
      this.requestTextFileInputFileVModel = [];
      this.newApiContext = new ApiFuzzContext();
    }
  }

  // Anonymous
  // Basic
  // Bearer,
  // ApiKey
  determineAuthnType(): string {

    if(this.securityBtnVisibility.anonymous == true)
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
