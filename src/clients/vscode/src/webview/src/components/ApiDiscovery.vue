<!-- https://pictogrammers.github.io/@mdi/font/6.9.96/ -->

<template>

    <!--v-card height affects Splitter in Master height="455px" -->
    <v-card
    color="white"
    outlined
    style="display: flex; flex-flow: column; height: 97%;">

     <!-- new context -->
     <Sidebar v-model:visible="newContextSideBarVisible" position="right" style="width:950px;">
      
      <div class="container-fluid">
        <div class="row mb-3"><h4>Create new Fuzz Context</h4></div>
        <div class="row">
            <div class="col-6">
              <form>
                <div class="form-group">
                  <v-text-field
                    v-model="newApiContext.name"
                    variant="underlined"
                    counter="40"
                    density="compact"
                    hint="e.g: my REST/GraphQL API"
                    label="Name"
                    maxlength="40"
                    clearable
                  ></v-text-field>
                </div>

              <v-divider />

              <h4>API Discovery</h4>
              
              <v-divider />
              <b>Request Message</b>
              <p><small>Tell Fuzzie about your API schema with Request Messages</small></p>
                
                <div class="mb-2" style="display:inline">
                  <div style="width: 100%; text-align:right;">
                    
                    <v-icon v-tooltip.right="'syntax is valid'" aria-hidden="false" color="green darken-2" v-show="(!requestMsgHasError)">
                    mdi-check-circle
                    </v-icon>
                    <v-icon  aria-hidden="false" color="red darken-2" v-show="requestMsgHasError" v-tooltip.right="'request message has error'">
                    mdi-close-circle
                    </v-icon>
                  </div>
                  <v-textarea 
                    label="Request Message" 
                    shaped
                    variant="outlined"
                    density="compact"
                    readonly
                    no-resize
                    style="border-color: rgba(192, 0, 250, 0.986);"
                    v-model="newApiContext.requestTextContent"
                     @click="(showReqMsgCreateDialog = true)"
                  />
                </div>
               
                <small>or load from Request Message file (.http, .rest or .fuzzie)</small>
                <div class="mb-2">
                  <v-file-input
                    v-model="requestTextFileInputFileVModel"
                    label="Request Message File"
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

                <!-- <div class="mb-2 mt-3">
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
                </div> -->
              </form>
            </div>
            <div class="col-6">
              
              <form>

                <h4>Global Headers - Authentication</h4>
                <v-divider />

                <div class="btn-group btn-group-sm" role="group" aria-label="Basic radio toggle button group">

                  <input type="radio" class="btn-check" name="btnradio" id="authn-noauthn" :checked="securityBtnVisibility.anonymous == true">
                  <label class="btn btn-outline-info small" for="authn-noauthn" @click="(
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

                <h4>Fuzz Properties</h4>
                <v-divider />
                
                <p><small>Number of fuzz tests to run per API operation</small></p>
                <v-divider />
                <v-slider
                  v-model="newApiContext.fuzzcaseToExec"
                  label=''
                  track-color="cyan"
                  thumb-color="cyan"
                  thumb-label="always"
                  min=1
                  max=500000
                  step="1"
                ></v-slider>
                <InputNumber
                            v-model="newApiContext.fuzzcaseToExec"
                            inputId="horizontal"
                            showButtons
                            buttonLayout="horizontal"
                            :step="1"
                            :min="1" :max="500000"
                            decrementButtonClass="p-button-outlined p-button-plain"
                            incrementButtonClass="p-button-outlined p-button-plain"
                            incrementButtonIcon="pi pi-plus"
                            decrementButtonIcon="pi pi-minus"                    
                        />
              </form>
              
              <v-divider />

              <div style="text-align:right">
                <button class="btn  btn-outline-info mr-3" @click="clearContextForm">Reset</button>
                <button class="btn  btn-outline-info" @click="createNewApiContext" :disabled="(createContextBtnDisable)">Create</button>
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
        <div class="row mb-3"><h4>Update Fuzz Context</h4></div>
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

              <h4>Test Properties</h4>
              <v-divider />

              <div class="form-group mb-3" >
                <v-text-field
                    v-model="apiContextEdit.hostname"
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

              <h4>API Discovery</h4>

              <v-divider />
              <b>Request Message (readonly)</b>
              <v-divider />

                <div class="mb-2">
                  <v-textarea 
                    label="Request Message" 
                    shaped
                    variant="outlined"
                    density="compact"
                    no-resize
                    readonly
                    v-model="apiContextEdit.requestTextContent"
                    @click="(showReqMsgReadOnlyDialog = true)"
                  ></v-textarea>
                  <small>Request Messages will not be updated, please create a new context or 
                    update individual API Operation
                  </small>
                </div>

                <!-- <div class="form-group">
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
                </div> -->
              </form>
            </div>
            <div class="col-6">
              
              <form>

                <h4>Global Headers - Authentication</h4>
                <v-divider />

                <div class="btn-group btn-group-sm" role="group" aria-label="Basic radio toggle button group">

                  <input type="radio" class="btn-check" name="btnradio" id="authn-noauthn" :checked="securityBtnVisibility.anonymous == true">
                  <label class="btn btn-outline-info small" for="authn-noauthn" @click="(
                    apiContextEdit.authnType='Anonymous',
                    securityBtnVisibility.anonymous = true,
                    securityBtnVisibility.basic=false,
                    securityBtnVisibility.bearer=false,
                    securityBtnVisibility.apikey=false
                  )">No Authentication</label>

                  <input type="radio" class="btn-check" name="btnradio" id="authn-basic" :checked="securityBtnVisibility.basic == true">
                  <label class="btn btn-outline-success small" for="authn-basic" @click="(
                    apiContextEdit.authnType='Basic',
                    securityBtnVisibility.anonymous=false,
                    securityBtnVisibility.basic=true,
                    securityBtnVisibility.bearer=false,
                    securityBtnVisibility.apikey=false
                  )">Basic Username/Password</label>

                  <input type="radio" class="btn-check" name="btnradio" id="authn-bearer" :checked="securityBtnVisibility.bearer == true">
                  <label class="btn btn-outline-success small" for="authn-bearer" @click="(
                    apiContextEdit.authnType='Bearer',
                    securityBtnVisibility.anonymous =false,
                    securityBtnVisibility.basic=false,
                    securityBtnVisibility.bearer=true,
                    securityBtnVisibility.apikey=false
                  )">Bearer Token</label>

                  <input type="radio" class="btn-check" name="btnradio" id="authn-apikey" :checked="securityBtnVisibility.apikey == true">
                  <label class="btn btn-outline-success small" for="authn-apikey" @click="(
                    apiContextEdit.authnType='ApiKey',
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

                <h4>Fuzz Properties</h4>
                <v-divider />
                <v-divider />

                <p><small>Number of fuzz tests to run per API operation</small></p>
                <v-divider />
                <v-slider
                  v-model="apiContextEdit.fuzzcaseToExec"
                  label=''
                  track-color="cyan"
                  thumb-color="cyan"
                  thumb-label="always"
                  min=1
                  max=500000
                  step="1"
                ></v-slider>
                <InputNumber
                            v-model="apiContextEdit.fuzzcaseToExec"
                            inputId="horizontal"
                            showButtons
                            buttonLayout="horizontal"
                            :step="1"
                            :min="1" :max="500000"
                            decrementButtonClass="p-button-outlined p-button-plain"
                            incrementButtonClass="p-button-outlined p-button-plain"
                            incrementButtonIcon="pi pi-plus"
                            decrementButtonIcon="pi pi-minus"                    
                        />
              </form>
              
              <v-divider />

              <div style="text-align:right">
                <button class="btn btn-outline-info" @click="updateApiContext">Update</button>
                
              </div>
            <!-- col end-->
            </div>
        </div>
      </div>
    </Sidebar>

    <!--request message dialog-->
    <Dialog v-model:visible="showReqMsgCreateDialog" 
      header="HTTP Request Message Editor" 
      :breakpoints="{ '960px': '75vw', '640px': '90vw' }" :style="{ width: '80vw' }"
      :maximizable="true" :modal="true"
      :dismissableMask="false" :closeOnEscape="false"
      @hide="onDialogClose(newApiContext.requestTextContent)">
      <Message severity="info">Ctrl + space to show intellisense for Fuzzie worklist types</Message>

      <div class="container-fluid">
        <div class="row">
          <div class="col text-left">
              <RequestMessageExampleView 
              v-bind:rqmsg:loadexample="newApiContext.requestTextContent"
              v-on:rqmsg:loadexample="newApiContext.requestTextContent = (newApiContext.requestTextContent == '' ? $event : newApiContext.requestTextContent + '\n###\n' + $event)" />
          </div>
          <div class="col text-right">
              <v-btn
                size="x-small"
                color="cyan"
                @click="parseRequestMessage(newApiContext.requestTextContent)"
                >
              Parse
              </v-btn>
              <v-icon v-tooltip.right="'syntax is valid'" aria-hidden="false" color="green darken-2" v-show="(!requestMsgHasError)">
                    mdi-check-circle
              </v-icon>
              <v-icon  aria-hidden="false" color="red darken-2" v-show="requestMsgHasError" v-tooltip.right="'request message has error'">
                mdi-close-circle
              </v-icon>
          </div>
        </div>
      </div>
      
      
      <div style="height: 10px;"></div>
      <codemirror
          v-model="newApiContext.requestTextContent"
          placeholder="request message goes here..."
          :style="{ height: '600px' }"
          :autofocus="true"
          :indent-with-tab="true"
          :tab-size="2"
          :extensions="extensions"
          @ready="onCMReady" 
        />
    </Dialog>

    <Dialog v-model:visible="showReqMsgReadOnlyDialog" 
      header="HTTP Request Message Editor" 
      :breakpoints="{ '960px': '75vw', '640px': '90vw' }" :style="{ width: '80vw' }"
      :maximizable="true" :modal="true"
      :dismissableMask="false">


          <codemirror
          v-model="apiContextEdit.requestTextContent"
          placeholder="request message goes here..."
          :style="{ height: '80vw' }"
          :autofocus="true"
          :indent-with-tab="true"
          :tab-size="2"
          :extensions="extensions"
          :options="cmOption"
        />
    </Dialog>

    

    <!-- Dialog delete API Context confirmation -->
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
          <button class="btn btn-outline-info mr-3" @click="showDeleteConfirmDialog = false">Cancel</button>
          <button class="btn btn-outline-danger" @click="deleteApiFuzzContext">Delete</button>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog delete FuzzCaseSetRun confirmation -->
    <v-dialog
      v-model="showDeleteFuzzCaseSetRunConfirmDialog"
      width="400"
    >
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Delete this Run?
        </v-card-title>

        <v-card-actions>
          <v-spacer></v-spacer>
          <button class="btn btn-outline-info mr-3" @click="showDeleteFuzzCaseSetRunConfirmDialog = false">Cancel</button>
          <button class="btn btn-outline-danger" @click="deleteApiFuzzCaseSetRun">Delete</button>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- fuzz confirmation -->
    <v-dialog
      v-model="showFuzzConfirmDialog"
      width="400"
    >
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Start Fuzzing
        </v-card-title>

        <v-card-actions>
          <v-spacer></v-spacer>
          <button class="btn btn-outline-info mr-3" @click="showFuzzConfirmDialog = false">Cancel</button>
          <button class="btn btn-outline-info" @click="fuzz">Fuzz</button>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-toolbar card color="#F6F6F6" flat density="compact" dense height="50px">

      <v-toolbar-title >Fuzz Contexts</v-toolbar-title>

      <v-btn color="accent" variant="plain" height="30px" plain icon
      :disabled="(!isGetFuzzContextFinish || !fuzzerConnected)"
        @click="(getFuzzcontexts)">
            <v-icon color="cyan darken-3">mdi-refresh</v-icon>
      </v-btn>

      <v-btn icon  variant="plain" height="30px" plain 
         :disabled="(!fuzzerConnected)"
         @click="(newContextSideBarVisible = true )">
        <v-icon color="cyan darken-3" icon="mdi-plus"></v-icon>
      </v-btn>

    </v-toolbar>

    
        
    <Tree :value="nodes"
        ref="tree"
        selectionMode="single" 
        :expandedKeys="expandedNodeKeys"
        v-show="showTree" 
        scrollHeight="320px" 
        style="height: 320px" class=" border-0">
          <template #default="slotProps" >

            <!--fuzz context-->
            <small v-show="slotProps.node.isFuzzCaseRun == false && slotProps.node.key != '-1' && slotProps.node.key != '-2'"
              :class="( (slotProps.node.isFuzzCaseRun == false && slotProps.node.key != '-1' && slotProps.node.key != '-2' &&
                slotProps.node.fuzzcontextId === selectedContextNode) ? 'p-1 border border-info border-2' : '')">
              <b 
                v-on:click="(onFuzzContextSelected(slotProps.node.fuzzcontextId),
                selectedContextNode = slotProps.node.fuzzcontextId)">
                {{slotProps.node.label}}
              </b>
            </small>

            <!--fuzz caseSetRun-->
            <small v-show="slotProps.node.isFuzzCaseRun == true && slotProps.node.key != '-1' && slotProps.node.key != '-2'"
              :class="( (
                  slotProps.node.isFuzzCaseRun == true && 
                  slotProps.node.key != '-1' && 
                  slotProps.node.key != '-2' &&
                  slotProps.node.fuzzcontextId == selectedContextNode &&
                  selectedCaseSetRunNode == slotProps.node.fuzzCaseSetRunsId) ? 'p-1 border border-info border-2' : '')">
              <b 
                v-on:click="( onFuzzCaseSetRunSelected(slotProps.node.fuzzcontextId, 
                slotProps.node.fuzzCaseSetRunsId,
                slotProps.node.hostname,
                slotProps.node.port),
                    selectedContextNode = slotProps.node.fuzzcontextId,
                    selectedCaseSetRunNode = slotProps.node.fuzzCaseSetRunsId)">
                {{slotProps.node.label}}
              </b>
              &nbsp;
              <v-icon
                  v-show="(!isFuzzingInProgress())"
                  variant="flat"
                  icon="mdi-delete"
                  color="cyan darken-3"
                  size="x-small"
                  @click="(
                    this.apiFuzzCaseSetRunToDelete = {
                      Id: slotProps.node.fuzzCaseSetRunsId
                    },
                    this.showDeleteFuzzCaseSetRunConfirmDialog = true
                  )">
                  </v-icon>
            </small>

            <span v-if="slotProps.node.key != '-1' && slotProps.node.key != '-2' && slotProps.node.isFuzzCaseRun == false">
                &nbsp;

                <div class="btn-group">
                  <v-icon
                  v-show="(!isFuzzingInProgress())"
                  variant="flat"
                  icon="mdi-cog-outline"
                  color="cyan darken-3"
                  size="x-small"
                  data-bs-toggle="dropdown">
                  </v-icon>
                  <ul class="dropdown-menu dropdown-menu-end">
                    <li><button class="dropdown-item" type="button" @click="(
                      onEditFuzzContextClicked(slotProps.node.data)
                    )">Edit</button></li>
                    <li><button class="dropdown-item" type="button" @click="(
                      onDeleteFuzzContextClicked(slotProps.node.fuzzcontextId, slotProps.node.name)
                    )">Delete</button></li>
                  </ul>
                </div>

                  &nbsp;

                  <v-icon
                  v-tooltip="'start fuzzing'"
                  v-show="(
                      isDataloadingCompleted &&
                      (currentFuzzingContextId == '' && currentFuzzingCaseSetRunId == '') && 
                      slotProps.node.isFuzzCaseRun == false)"
                  variant="flat"
                  icon="mdi-lightning-bolt"
                  color="cyan darken-3"
                  size="x-small"
                  @click="(
                    onFuzzIconClicked(
                      slotProps.node.fuzzcontextId,
                      slotProps.node.name)
                  )" />

                  <v-icon
                  v-tooltip="'cancel fuzzing'"
                  v-show="( (currentFuzzingContextId != '' && currentFuzzingCaseSetRunId != '') )"
                  variant="flat"
                  icon="mdi-cancel"
                  color="cyan darken-3"
                  size="x-small"
                  @click="(
                    onCancelFuzzIconClicked()
                  )" />
                  

              </span>

              <v-progress-linear
                indeterminate
                color="cyan"
                v-show="(
                  slotProps.node.isFuzzCaseRun == false &&
                  this.currentFuzzingContextId == slotProps.node.fuzzcontextId)"
                style="width:100%" />
              
              <v-progress-linear
                indeterminate
                color="cyan"
                v-show="(
                  slotProps.node.isFuzzCaseRun == true &&
                  this.currentFuzzingCaseSetRunId == slotProps.node.fuzzCaseSetRunsId)"
                style="width:100%" />

          </template>
      </Tree>
    </v-card>
</template>

<script lang="ts">
import { inject } from 'vue';
import { Options, Vue } from 'vue-class-component';
import Tree, { TreeNode } from 'primevue/tree';
import dateformat from 'dateformat';
import Sidebar from 'primevue/sidebar';
import Dialog from 'primevue/dialog';
import Message from 'primevue/message';
import InputNumber from 'primevue/inputnumber';
import Dropdown from 'primevue/dropdown';
import RequestMessageExampleView from './RequestMessageExampleView.vue';
import Utils from '../Utils';
import { ApiFuzzContext, ApiFuzzContextUpdate } from '../Model';
import FuzzerWebClient from "../services/FuzzerWebClient";
import FuzzerManager from "../services/FuzzerManager";
import moment from 'moment';

class Props {
  // optional prop
  toastInfo: any = {};
  toastError: any = {};
  toastSuccess: any = {};
  eventemitter: any = {};
  fuzzermanager: FuzzerManager;
  webclient : FuzzerWebClient;
}

@Options({
  components: {
    Tree,
    Sidebar,
    Dialog,
    Message,
    InputNumber,
    Dropdown,
    RequestMessageExampleView
  },
})


export default class ApiDiscovery extends Vue.with(Props) {
  
  $logger;
  openapi3FileInputFileVModel: Array<any> = [];
  requestTextFileInputFileVModel: Array<any>  = [];
  requestTextEditFileInputVModel: Array<any> = [];
  showPasswordValue = false;
  fuzzcontexts: Array<ApiFuzzContext> = [];
  nodes: TreeNode[] = [];
  expandedNodeKeys = {};
  showTree = this.nodes.length > 0 ? "true": "false";
  showDeleteConfirmDialog = false;
  showDeleteFuzzCaseSetRunConfirmDialog = false;
  showFuzzConfirmDialog = false;
  showReqMsgCreateDialog = false;
  showReqMsgReadOnlyDialog = false;
  newContextSideBarVisible = false;
  updateContextSideBarVisible = false;
  isGetFuzzContextFinish = true;
  createContextBtnDisable = false;
  apiContextToDelete: any = {};
  apiFuzzCaseSetRunToDelete: any = {};
  apiContextIdToFuzz = '';
  inputRules= [
        v => v.length <= 40 || 'Max 40 characters'
  ];
  requestMsgHasError = false;
  requestMsgErrorMessage = ''

  selectedContextNode = ''
  selectedCaseSetRunNode = ''
  
  fuzzerConnected = false;
  currentFuzzingContextId = '';
  currentFuzzingCaseSetRunId = '';
  isDataloadingCompleted = false;

  showFuzzIcon = true;
  showCancelFuzzIcon = false;
  showFuzzProgressBar = false;

  isDataLoading = false;

  securityBtnVisibility = {
    anonymous: true,
    basic: false,
    bearer: false,
    apikey: false

  }

  newApiContext= new ApiFuzzContext();
  apiContextEdit = new ApiFuzzContext();

  cmOption = {
        tabSize: 4,
        styleActiveLine: true,
        autofocus: true,
        lineNumbers: true,
        line: true,
        foldGutter: true,
        styleSelectedText: true,
        mode: "text/x-mysql",
        keyMap: "sublime",
        matchBrackets: true,
        showCursorWhenSelecting: true,
        extraKeys: { Ctrl: "autocomplete" }
    };

  //methods
  
  beforeMount(){
    this.$logger = inject('$logger');
  }

  async mounted() {

    this.eventemitter.on('fuzzer.ready', this.onFuzzerReady);
    this.eventemitter.on('fuzzer.notready', this.onFuzzerNotReady);
    this.eventemitter.on('fuzz.start', this.onFuzzStart);
    this.eventemitter.on('fuzz.once.stop', this.onFuzzOnceStop);
    
    this.eventemitter.on('fuzz.stop', this.onFuzzStop);
    this.eventemitter.on('onFuzzCaseSetUpdated', this.onFuzzCaseSetUpdated);

    this.eventemitter.on('fuzzer.dataloading.complete', this.onDataloadingCompleted);

    this.getFuzzcontexts()
  }

  onFuzzerReady() {
    this.fuzzerConnected = true;
    this.getFuzzcontexts();
  }

  onFuzzerNotReady() {
    this.clearData();
    this.isDataloadingCompleted = false;
    this.fuzzerConnected = false;
    this.currentFuzzingContextId = '';
    this.currentFuzzingCaseSetRunId = ''
  }

  onDataloadingCompleted() {
    this.isDataloadingCompleted = true;
  }

  //constantly receiving event
  async onFuzzStart(data) {

    await this.getFuzzcontexts();

    const fuzzContextId = data.fuzzContextId;
    const fuzzCaseSetRunId = data.fuzzCaseSetRunId;

    if(this.currentFuzzingContextId != '' && this.currentFuzzingCaseSetRunId != ''){
      return;
    }

    this.currentFuzzingContextId = fuzzContextId;
    this.currentFuzzingCaseSetRunId = fuzzCaseSetRunId;

    this.selectedContextNode = fuzzContextId;
    this.selectedCaseSetRunNode =fuzzCaseSetRunId;

  }


  async onFuzzOnceStop() {
    await this.getFuzzcontexts();
  }

  async onFuzzStop() {
    this.onFuzzCaseSetRunSelected(this.currentFuzzingContextId, this.currentFuzzingCaseSetRunId);
    this.currentFuzzingContextId = '';
    this.currentFuzzingCaseSetRunId = ''
  }

  //#### websocket event ends ####

  onEditFuzzContextClicked(data) {
    this.apiContextEdit = data;
    this.updateContextSideBarVisible = true;
  }

  onDeleteFuzzContextClicked(fuzzcontextId, name) {
    this.apiContextToDelete = {
                          Id: fuzzcontextId,
                          name: name,
                        },
    this.showDeleteConfirmDialog = true
  }


  onFuzzFuzzContextClicked(fuzzcontextId: string) {
    this.apiContextIdToFuzz = fuzzcontextId;
    this.showFuzzConfirmDialog = true
  }

  onFuzzCaseSetUpdated(fuzzContextId) {
    this.getFuzzcontexts();
    //send event to FuzzCaseSet pane to show fuzzcaseset-run-summaries for current fuzzCaseSetRun that is fuzzing
    this.eventemitter.emit("onFuzzContextSelected", fuzzContextId, '');
  }

  async getFuzzcontexts() {

    try {

        if(!this.fuzzerConnected || this.isDataLoading) {
          return;
        }

        this.isDataLoading = true;

        this.isGetFuzzContextFinish = false;
        const [OK, err, fcs] = await this.fuzzermanager.getFuzzcontexts()    

        if (OK)
        {
          this.fuzzcontexts = fcs;
          this.nodes = [];
          this.nodes = this.createTreeNodesFromFuzzcontexts(fcs);

          //this.eventemitter.emit('onFuzzContextRefreshClicked');
          
        }
        else
        {
          this.toastError(err, 'Get Fuzz Context');
        }

        this.isGetFuzzContextFinish = true;

    } catch (error) {
        //TODO: log
        console.log(error)
    }
    finally{
      this.isDataLoading = false;
    }
  }

  createTreeNodesFromFuzzcontexts(fcs: ApiFuzzContext[]): TreeNode[] {

    this.expandedNodeKeys = {};
    this.expandedNodeKeys['-1'] = true;
    this.expandedNodeKeys['-2'] = true;

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

    //sort fuzz-context by datetime
    fcs.sort(function(a: ApiFuzzContext,b: ApiFuzzContext) {

      const l = new Date(a.datetime);
      const r = new Date(b.datetime);
      // Turn your strings into dates, and then subtract them
      // to get a value that is either negative, positive, or zero.
      return l.getTime() - r.getTime();
    });
    //sort fuzzcaseset by starttime
    fcs.forEach(fc => {
      fc.fuzzCaseSetRuns.sort(function(a,b) {

      const l = new Date(a.startTime);
      const r = new Date(b.startTime);
      // Turn your strings into dates, and then subtract them
      // to get a value that is either negative, positive, or zero.
      return r.getTime() - l.getTime();
    });
    })
    
    //create node in Primevue Tree
    fcs.forEach(fc => {

        if(fc instanceof ApiFuzzContext)
        {
            // fuzz-context
            const fcNode: any = {
              key: fc.Id,
              fuzzcontextId: fc.Id,
              label: fc.name,
              name: fc.name,
              data: fc,
              isFuzzCaseRun: false,
              hostname: fc.hostname,
              port: fc.port
            };

            this.expandedNodeKeys[fc.Id] = true;

            apiNode.children.push(fcNode);

            fc.fuzzCaseSetRuns.forEach(fcsr => {
            
            // fuzz-case-set-run
            const casesetNode = {
              key: fcsr.fuzzCaseSetRunsId,
              fuzzcontextId: fcsr.fuzzcontextId,
              fuzzCaseSetRunsId: fcsr.fuzzCaseSetRunsId,
              isFuzzing: false,
              label: moment(new Date(fcsr.startTime), 'YYYY-MM-DD hh:mm:ss').startOf('second').fromNow(),//dateformat(fcsr.startTime, "dS mmm, yy - H:MM:ss"), //`${nodeLabel.toLocaleDateString('en-us')} ${nodeLabel.toLocaleTimeString()}`,
              data: fcsr,
              isFuzzCaseRun: true,
              hostname: fc.hostname,
              port: fc.port
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

  async onDialogClose(rqMsg: string) {
    this.parseRequestMessage(rqMsg);
  }

  async parseRequestMessage(rqMsg) {
    if(rqMsg == ''){
      return;
    }
    const [ok, error] = await this.webclient.parseRequestMessage(btoa(rqMsg));

    if(!ok) {
      this.requestMsgHasError = true;
      this.requestMsgErrorMessage = error;
      this.toastError(error);
      return;
    }
    this.requestMsgErrorMessage = '';
    this.requestMsgHasError = false;
  }

  async onFuzzIconClicked (fuzzcontextId, name)  {

    if(!this.isDataloadingCompleted) {
      this.toastInfo('please wait for fuzz data loading to complete');
    }

    await this.webclient.fuzz(fuzzcontextId)

    this.toastInfo(`initiatiated fuzzing on ${name}`);

  }

  async onCancelFuzzIconClicked() {
    
    this.toastInfo('cancelling fuzzing');

    const ok = await this.webclient.cancelFuzzing();

    if(!ok) {
      this.toastError('cancel fuzzing failed due to an internal error, please reopen webview');
      return;
    }

    this.currentFuzzingContextId = '';
    this.currentFuzzingCaseSetRunId = ''
 }

  onFuzzContextSelected(fuzzcontextId) {
    this.eventemitter.emit("onFuzzContextSelected", fuzzcontextId);
  }

  onFuzzCaseSetRunSelected(fuzzcontextId, fuzzCaseSetRunsId) {
    this.eventemitter.emit("onFuzzCaseSetRunSelected", fuzzcontextId, fuzzCaseSetRunsId);
  }

  async onRequestTextFileChange(event) {

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
      this.toastError('Request Text file has ext of .http, .text or .fuzzie', 'Invalid File Type');
    }
  }


  async onOpenApi3FileChange(event) {

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
      this.toastError('OpenAPI3 spec files are yaml or json', 'Invalid File Type');
    }
  }

  

  async onRequestMessageFileChange(event) {

    const files = event.target.files;

    const file = files[0];

    const reader = new FileReader();
    if (file.name.includes(".http") || file.name.includes(".fuzzie") || file.name.includes(".rest")) {

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
      this.toastError('Request Message files must be either .http, .rest or .fuzzie', 'Invalid File Type');
    }
  }


  async deleteApiFuzzContext() {

    if(!this.fuzzerConnected){
          return;
    }

      const id = this.apiContextToDelete.Id;
      const [ok, error] = await this.fuzzermanager.deleteApiFuzzContext(id);

    if(!ok)
    {
      this.toastError(error, 'Delete API FuzzContext');
    }
    else
    {
      this.eventemitter.emit("onFuzzContextDelete", id);

      this.getFuzzcontexts();

      this.toastSuccess(`${this.apiContextToDelete.name} deleted successfully`, '');
    }

    this.showDeleteConfirmDialog = false;
    this.apiContextToDelete = {};
  }

  async deleteApiFuzzCaseSetRun() {
    if(!this.fuzzerConnected){
          return;
    }

      const fuzzCaseSetRunId = this.apiFuzzCaseSetRunToDelete.Id;
      const [ok, error] = await this.webclient.deleteApiFuzzCaseSetRun(fuzzCaseSetRunId);

      this.eventemitter.emit("onFuzzCaseRunDeleted", fuzzCaseSetRunId);

    if(!ok)
    {
      this.toastError(error, 'Delete Fuzz Run');
    }
    else
    {

      this.getFuzzcontexts();

      this.toastSuccess(`deleted successfully`, '');
    }

    this.showDeleteFuzzCaseSetRunConfirmDialog = false;
    this.apiFuzzCaseSetRunToDelete = {};
  }

  async updateApiContext() {

    if(!this.fuzzerConnected){
          return;
    }

    const apiFCUpdate = new ApiFuzzContextUpdate();
    
    apiFCUpdate.fuzzcontextId = this.apiContextEdit.Id;

    Utils.mapProp(this.apiContextEdit, apiFCUpdate);

    const [ok, error] = await this.webclient.updateApiFuzzContext(apiFCUpdate);

    if(!ok)
    {
      this.toastError(error, 'Update API FuzzContext');
    }
    else
    {
      this.apiContextEdit = new ApiFuzzContext();

      this.toastSuccess(`${apiFCUpdate.name} updated successfully`, '');
    }

    this.updateContextSideBarVisible = false;
  }

  async createNewApiContext() {

    if(!this.fuzzerConnected){
          return;
    }

    try {

        this.createContextBtnDisable = true;
    
        this.newApiContext.authnType = this.determineAuthnType();

        this.newApiContext.apiDiscoveryMethod = this.determineApiDiscoveryMethod();

        if(this.newApiContext.name == '') // || this.newApiContext.hostname == '' || this.newApiContext.port == undefined)
        {
          this.toastError('Name is required');
          return;
        }

        if(this.newApiContext.requestTextContent == '' || this.requestMsgHasError == true)
        {
          this.toastError('Request Message is either empty or has error', 'API Discovery');
          return;
        }

        // if(this.newApiContext.openapi3Url != '') {
        //   const [ok, error, data] = await this.fuzzermanager.httpGetOpenApi3FromUrl(this.newApiContext.openapi3Url)

        //   if(!ok)
        //   {
        //     this.toastError(error, 'Trying to get OpenApi3 spec by Url');

        //     return;
        //   }

        //   this.newApiContext.openapi3Content = data;

        // }

        // if(this.newApiContext.openapi3Content == '' && this.newApiContext.requestTextContent == '')
        // {
        //   this.toastError('need either OpenAPI 3 spec or Request Text to create context', 'API Discovery');
        //   return;
        // }
      
        const apifc: ApiFuzzContext = Utils.copy(this.newApiContext);
        apifc.openapi3Content = apifc.openapi3Content != '' ? btoa(apifc.openapi3Content) : '';
        apifc.requestTextContent = apifc.requestTextContent != '' ? btoa(apifc.requestTextContent) : '';

        const result =  await this.fuzzermanager.newFuzzContext(apifc);
        const ok = result['ok'];
        const error =result['error'];

        if(!ok && error != '')
        {
          this.toastError(error, 'Create new API context');
          return;
        }
        else
        {
          this.newContextSideBarVisible = false;
          this.getFuzzcontexts();

          this.toastSuccess(error, 'API Fuzz Context created');

          //reset form
          this.openapi3FileInputFileVModel = [];
          this.requestTextFileInputFileVModel = [];
          this.newApiContext = new ApiFuzzContext();
          this.requestMsgHasError = false;
          this.securityBtnVisibility.anonymous = true,
          this.securityBtnVisibility.basic=false,
          this.securityBtnVisibility.bearer=false,
          this.securityBtnVisibility.apikey=false
        }

    } catch (error) {
      this.$logger.error(error);
    }
    finally {
      this.createContextBtnDisable = false;
    }
  }

  isFuzzingInProgress() {
    if(this.currentFuzzingCaseSetRunId != '' && this.currentFuzzingContextId != '') {
      return true;
    }
    return false;
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
        return 'request_message';
    }
    return 'openapi3';
  }

  clearData() {
    this.fuzzcontexts = [];
    this.nodes = [];
    this.selectedContextNode = '';
    this.selectedCaseSetRunNode = '';
    this.clearContextForm();
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

.v-text-field--outlined fieldset {
    color: red !important;
}

.ui-button {
	background-color: cyan!important;
	color: cyan!important;
}

</style>
