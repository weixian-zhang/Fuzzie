

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
                  @click="(loadExample('get-multiple-1'))">GET</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('get-path'))">GET - Path</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('get-path-qs'))">GET - Path & Querystring</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('get-path-mutate-1'))">GET - Mutate Path</a>
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
                  @click="(loadExample('post-file'))">Upload File: file with naughty content</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('post-pdf'))">Upload File: PDF</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('post-image'))">Upload File: Image</a>
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
                  @click="(loadExample('gql-query-no-var-1'))">GraphQL Query</a>
                  </li>

                  <li><a class="dropdown-item" href="#"
                  @click="(loadExample('gql-mutation-var-1'))">GraphQL Mutate with Variables</a>
                  </li>

                  <li><a class="dropdown-item" href="#"
                  @click="(loadExample('mutate-post-json'))">Mutate your input - JSON</a>
                  </li>
                  <li><a class="dropdown-item" href="#"
                  @click="(loadExample('mutate-post-xml'))">Mutate your input - XML</a>
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