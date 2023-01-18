

<template>
    <div class="container-fluid width=100%">
          <div class="row">
            <div class="col-6">
              <div class="btn-group">
                <button type="button" class="btn btn-info btn-sm dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                  examples
                </button>
                <ul class="dropdown-menu">
                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('get'))">GET</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('post'))">POST</a>
                  </li>

                  <li><a class="dropdown-item" href="#"
                  @click="(loadExample('file-upload-myfile-batchfile'))">Upload File: custom file content - delimited batch-file</a>
                  </li>

                  <li><a class="dropdown-item" href="#"
                  @click="(loadExample('file-upload-myfile-json'))">Upload File: custom file content - JSON</a>
                  </li>

                  <li><a class="dropdown-item" href="#"
                  @click="(loadExample('file-upload-myfile-wordlisttypes'))">Upload File: custom file content - primitive wordlist-type support</a>
                  </li>

                  <li><a class="dropdown-item" href="#"
                  @click="(loadExample('graphql-query'))">GraphQL Query</a>
                  </li>

                  <li><a class="dropdown-item" href="#"
                  @click="(loadExample('graphql-mutate'))">GraphQL Mutate</a>
                  </li>
                </ul>
              </div>
            </div>
            <div class="col-6 text-right">
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
</template>


<script lang="ts">
import { Options, Vue  } from 'vue-class-component';
import RequestMessageExamples from './RequestMessageExamples';

class Props {
}

@Options({
  components: {

  },
  watch: {

  }
})

 export default class RequestMessageExampleView extends Vue.with(Props) {
    reqMsgExampleLoader = new RequestMessageExamples();

    loadExample(key) {
      const example = this.reqMsgExampleLoader.loadExample(key);
      this.$emit('rqmsg:loadexample', example);
    }
 }

</script>

 <style scoped>
 </style>