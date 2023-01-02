<!-- https://pictogrammers.github.io/@mdi/font/6.9.96/ -->

<template>

    <!--v-card height affects Splitter in Master height="455px" -->
    <v-card
    color="white"
    outlined
    style="display: flex; flex-flow: column; height: 100%;">

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

              <b>API Discovery</b>
              <p><small>Tell Fuzzie about your API schema in one of the following ways</small></p>
              <v-divider />

                <div class="mb-2" style="display:inline">
                  <v-textarea 
                    label="Request Message" 
                    shaped
                    variant="outlined"
                    density="compact"
                    readonly
                    no-resize
                    v-model="newApiContext.requestTextContent"
                     @click="(showReqMsgEditDialog = true)"
                  />
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

                <b>Fuzz Properties</b>
                <v-divider />
                <v-divider />
                
                <v-slider
                  v-model="newApiContext.fuzzcaseToExec"
                  label=''
                  track-color="cyan"
                  thumb-color="cyan"
                  thumb-label="always"
                  min=100
                  max=50000
                  step="5"
                ></v-slider>

              </form>
              
              <v-divider />

              <div style="text-align:right">
                <button class="btn  btn-outline-info mr-3" @click="clearContextForm">Reset</button>
                <button class="btn  btn-outline-info" @click="createNewApiContext">Create</button>
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
        <div class="row mb-3"><h5>Update Fuzz Context</h5></div>
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

              <b>Test Properties</b>
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

              <b>API Discovery (Read-Only)</b>
              <p><small>Tell Fuzzie about your API schema in one of the following ways</small></p>
              <v-divider />

                <div class="mb-2">
                  <v-textarea 
                    label="Request Message" 
                    shaped
                    variant="outlined"
                    density="compact"
                    readonly
                    no-resize
                    v-model="apiContextEdit.requestTextContent"
                    @click="(showReqMsgReadOnlyDialog = true)"
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

                <b>Fuzz Properties</b>
                <v-divider />
                <v-divider />
                
                <v-slider
                  v-model="apiContextEdit.fuzzcaseToExec"
                  label=''
                  track-color="cyan"
                  thumb-color="cyan"
                  thumb-label="always"
                  min=100
                  max=50000
                  step="5"
                ></v-slider>

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
    <Dialog v-model:visible="showReqMsgEditDialog" 
      header="Request Message" 
      :breakpoints="{ '960px': '75vw', '640px': '90vw' }" :style="{ width: '80vw' }"
      :maximizable="true" :modal="true">
      <Message severity="info">Ctrl + space to show intellisense for Fuzzie worklist types</Message>

      <div class="display:inline-block fill-height">
        <v-btn
          size="x-small"
          color="cyan"
          @click="(newApiContext.requestTextContent=this.reqMsgExampleLoader.loadExample('get'))">
          GET example
        </v-btn>
        <v-btn
          size="x-small"
          color="cyan"
          class="ml-5"
          @click="(newApiContext.requestTextContent=this.reqMsgExampleLoader.loadExample('post'))">
          POST example
        </v-btn>
      </div>

      <div style="height: 10px;"></div>
      <codemirror
          v-model="newApiContext.requestTextContent"
          placeholder="request message goes here..."
          :style="{ height: '80vw' }"
          :autofocus="true"
          :indent-with-tab="true"
          :tab-size="2"
          :extensions="extensions"
          @ready="onCMReady" 
        />
              <!-- <v-textarea 
                    label="" 
                    shaped
                    variant="outlined"
                    auto-grow
                    no-resize
                    v-model="newApiContext.requestTextContent"
                     density="compact" 
                     rows="40"/>
              <template #footer>
                  <Button label="No" icon="pi pi-times" @click="closeBasic2" class="p-button-text" />
                  <Button label="Yes" icon="pi pi-check" @click="closeBasic2" autofocus />
              </template> -->
    </Dialog>

    <Dialog v-model:visible="showReqMsgReadOnlyDialog" 
      header="Request Message" 
      :breakpoints="{ '960px': '75vw', '640px': '90vw' }" :style="{ width: '80vw' }"
      :maximizable="true" :modal="true">

<!-- codemirror vuejs example
  https://codemirror.net/examples/autocompletion/
  https://codemirror.net/docs/guide/
  https://github.com/surmon-china/vue-codemirror/issues/66-->

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

              <!-- <v-textarea 
                    label="" 
                    shaped
                    variant="outlined"
                    auto-grow
                    readonly
                    no-resize
                    v-model="apiContextEdit.requestTextContent"
                     density="compact" 
                     rows="40"/>
              <template #footer>
                  <Button label="No" icon="pi pi-times" @click="closeBasic2" class="p-button-text" />
                  <Button label="Yes" icon="pi pi-check" @click="closeBasic2" autofocus />
              </template> -->
    </Dialog>

    

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
          <button class="btn btn-outline-info mr-3" @click="showDeleteConfirmDialog = false">Cancel</button>
          <button class="btn btn-outline-danger" @click="deleteApiFuzzContext">Delete</button>
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

      <!-- <v-btn  variant="plain" height="30px" plain icon v-tooltip.bottom="'create new messaging fuzz context (in roadmap)'">
        <v-icon color="cyan darken-3">mdi-message-plus-outline</v-icon>
      </v-btn> -->

      <v-btn color="accent" variant="plain" height="30px" plain icon v-tooltip.right="'refresh fuzz contexts'"
      :disabled="!isGetFuzzContextFinish"
        @click="getFuzzcontexts">
            <v-icon color="cyan darken-3">mdi-refresh</v-icon>
      </v-btn>

      <v-btn v-tooltip.bottom="'create new API fuzz context'" icon  variant="plain" height="30px" plain 
         @click="(newContextSideBarVisible = true )">
        <v-icon color="cyan darken-3">mdi-api</v-icon>
      </v-btn>

    </v-toolbar>
        
        <Tree :value="nodes" selectionMode="single" :expandedKeys="expandedNodeKeys" v-show="showTree" scrollHeight="320px" class="border-0">
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
                v-on:click="( onFuzzCaseSetRunSelected(slotProps.node.fuzzcontextId, slotProps.node.fuzzCaseSetRunsId),
                    selectedContextNode = slotProps.node.fuzzcontextId,
                    selectedCaseSetRunNode = slotProps.node.fuzzCaseSetRunsId)">
                {{slotProps.node.label}}
              </b>
            </small>

            <span v-if="slotProps.node.key != '-1' && slotProps.node.key != '-2' && slotProps.node.isFuzzCaseRun == false">
                &nbsp;
                <v-icon
                  variant="flat"
                  icon="mdi-pencil"
                  color="cyan darken-3"
                  size="x-small"
                  @click="(
                    onEditFuzzContextClicked(slotProps.node.data)
                  )"
                  >

                  </v-icon>
                  &nbsp;
                  <v-icon
                  variant="flat"
                  icon="mdi-delete"
                  color="cyan darken-3"
                  size="x-small"
                  @click="(
                    onDeleteFuzzContextClicked(slotProps.node.fuzzcontextId, slotProps.node.name)
                  )"/>

                  &nbsp;

                  <v-icon
                  v-tooltip="'start fuzzing'"
                  v-show="(
                      isFuzzingInProgress() == false && 
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
                  v-show="( isFuzzingInProgress() == true)"
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

import { Options, Vue } from 'vue-class-component';
import Tree, { TreeNode } from 'primevue/tree';
import dateformat from 'dateformat';
import Sidebar from 'primevue/sidebar';
import Dialog from 'primevue/dialog';
import Message from 'primevue/message';

import RequestMessageExamples from './RequestMessageExamples';
import Utils from '../Utils';
import { ApiFuzzContext, ApiFuzzContextUpdate } from '../Model';
import FuzzerWebClient from "../services/FuzzerWebClient";
import FuzzerManager from "../services/FuzzerManager";

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
    Message
  },
})


export default class ApiDiscovery extends Vue.with(Props) {
  
  openapi3FileInputFileVModel: Array<any> = [];
  requestTextFileInputFileVModel: Array<any>  = [];
  showPasswordValue = false;
  nodes: TreeNode[] = [];
  expandedNodeKeys = {};
  showTree = this.nodes.length > 0 ? "true": "false";
  showDeleteConfirmDialog = false;
  showFuzzConfirmDialog = false;
  showReqMsgEditDialog = false;
  showReqMsgReadOnlyDialog = false;
  newContextSideBarVisible = false;
  updateContextSideBarVisible = false;
  isGetFuzzContextFinish = true;
  apiContextToDelete: any = {};
  apiContextIdToFuzz = '';
  inputRules= [
        () => !!Utils.isValidHttpUrl(this.newApiContext.openapi3Url) || "URL is not valid"
  ];

  selectedContextNode = ''
  selectedCaseSetRunNode = ''
  
  fuzzerConnected = false;
  currentFuzzingContextId = '';
  currentFuzzingCaseSetRunId = '';

  showFuzzIcon = true;
  showCancelFuzzIcon = false;
  showFuzzProgressBar = false;

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

  reqMsgExampleLoader = new RequestMessageExamples()

  //methods
  
  async mounted() {

    this.eventemitter.on('fuzzer.ready', this.onFuzzStartReady);
    this.eventemitter.on('fuzzer.notready', this.onFuzzerNotReady);
    this.eventemitter.on('fuzz.start', this.onFuzzStart);
    this.eventemitter.on('fuzz.stop', this.onFuzzStop);

    this.getFuzzcontexts()

    // const jsDocCompletions = jsonLanguage.data.of({
    //   autocomplete: this.completeJSDoc
    // })
  }

  // #### websocket events ####

  onFuzzStartReady() {
      
    this.fuzzerConnected = true;
    this.getFuzzcontexts();
  }

  onFuzzerNotReady() {
    //this.clearData()
    this.fuzzerConnected = false;
    this.currentFuzzingContextId = '';
    this.currentFuzzingCaseSetRunId = ''
  }

  //constantly receiving event
  onFuzzStart(data) {

    const fuzzContextId = data.fuzzContextId;
    const fuzzCaseSetRunId = data.fuzzCaseSetRunId;

    if(this.currentFuzzingContextId != '' && this.currentFuzzingCaseSetRunId != ''){
      return;
    }

    this.currentFuzzingContextId = fuzzContextId;
    this.currentFuzzingCaseSetRunId = fuzzCaseSetRunId;

    this.selectedContextNode = fuzzContextId;
    this.selectedCaseSetRunNode =fuzzCaseSetRunId;

    this.getFuzzcontexts();

    //send event to FuzzCaseSet pane to show fuzzcaseset-run-summaries for current fuzzCaseSetRun that is fuzzing
    this.eventemitter.emit("onFuzzContextSelected", fuzzContextId, fuzzCaseSetRunId);

    this.toastInfo('fuzzing started');
  }

  onFuzzStop() {

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

  
  async getFuzzcontexts() {

    try {

        if(!this.fuzzerConnected){
          return;
        }

        this.isGetFuzzContextFinish = false;
        const [OK, err, fcs] = await this.fuzzermanager.getFuzzcontexts()    

        if (OK)
        {
          this.nodes = [];
          this.nodes = this.createTreeNodesFromFuzzcontexts(fcs);

          this.eventemitter.emit('onFuzzContextRefreshClicked');
          
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
              isFuzzCaseRun: false
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
              label: dateformat(fcsr.startTime, "ddd, mmm dS, yy - h:MM:ss TT"), //`${nodeLabel.toLocaleDateString('en-us')} ${nodeLabel.toLocaleTimeString()}`,
              data: fcsr,
              isFuzzCaseRun: true
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


  async onFuzzIconClicked (fuzzcontextId, name)  {

    this.toastInfo(`initiatiated fuzzing on ${name}`);

    const [ok, msg] = await this.webclient.fuzz(fuzzcontextId)
    if(!ok) {
      this.toastError(`error when start fuzzing: ${msg}`, 'Fuzzing');
      return;
    }
  }

  isFuzzingInProgress() {
    if(this.currentFuzzingContextId != '' &&  this.currentFuzzingCaseSetRunId != '') {
      return true;
    }
    return false;
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
      this.toastError('Request Text file has ext of .http, .text or .fuzzie', 'Invalid File Type');
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
      this.toastError('OpenAPI3 spec files are yaml or json', 'Invalid File Type');
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

      this.toastSuccess(`${this.apiContextToDelete.name} updated successfully`, 'Delete API FuzzContext');
    }

    this.showDeleteConfirmDialog = false;
    this.apiContextToDelete = {};
  }

  async updateApiContext() {

    if(!this.fuzzerConnected){
          return;
    }

    const apiFCUpdate = new ApiFuzzContextUpdate();
    
    apiFCUpdate.fuzzcontextId = this.apiContextEdit.Id;

    Utils.mapProp(this.apiContextEdit, apiFCUpdate);

    const [ok, error] = await this.fuzzermanager.updateApiFuzzContext(apiFCUpdate);

    if(!ok)
    {
      this.toastError(error, 'Update API FuzzContext');
    }
    else
    {
      this.apiContextEdit = new ApiFuzzContext();

      this.toastSuccess(`${apiFCUpdate.name} updated successfully`, 'Update API FuzzContext');
    }

    this.updateContextSideBarVisible = false;
  }

  async createNewApiContext() {

    if(!this.fuzzerConnected){
          return;
    }
    
    this.newApiContext.authnType = this.determineAuthnType();

    this.newApiContext.apiDiscoveryMethod = this.determineApiDiscoveryMethod();

    if(this.newApiContext.name == '' || this.newApiContext.hostname == '' || this.newApiContext.port == undefined)
    {
      this.toastError('Name, hostname, port are required', 'New API Context - Missing Info');
      return;
    }

    if(this.newApiContext.openapi3Url != '') {
      const [ok, error, data] = await this.fuzzermanager.httpGetOpenApi3FromUrl(this.newApiContext.openapi3Url)

      if(!ok)
      {
        this.toastError(error, 'Trying to get OpenApi3 spec by Url');

        return;
      }

      this.newApiContext.openapi3Content = data;

    }

    if(this.newApiContext.openapi3Content == '' && this.newApiContext.requestTextContent == '')
    {
      this.toastError('need either OpenAPI 3 spec or Request Text to create context', 'API Discovery');
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
        return 'request_message';
    }
    return 'openapi3';
  }

  clearData() {
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

</style>
