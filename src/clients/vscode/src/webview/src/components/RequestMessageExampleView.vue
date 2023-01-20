

<template>
    <div class="container-fluid width=100%">
          <div class="row">
            <div class="col-6">
              <div class="btn-group">
                <button type="button" class="btn btn-info btn-sm dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                  samples
                </button>
                <ul class="dropdown-menu">
                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('get'))">GET</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('post-json'))">POST JSON</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('post-xml'))">POST XML</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('post-xwwwformurlencoded'))">POST x-www-form-urlencoded</a>
                  </li>
                  
                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('post-pdf'))">POST a PDF</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('post-image'))">POST an Image</a>
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

    requestMsgHasError = false;
    requestMsgErrorMessage = '';

    loadExample(key) {
      const example = this.reqMsgExampleLoader.loadExample(key);
      this.$emit('rqmsg:loadexample', example);
    }


 }

</script>

 <style scoped>
 </style>