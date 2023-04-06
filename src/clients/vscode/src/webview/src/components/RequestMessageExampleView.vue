

<template>
    <div class="container-fluid width=100%">
          <div class="row">
            <div class="col">

              <div class="btn-group">
                <button type="button" class="btn btn-info btn-sm dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                  GET
                </button>
                <ul class="dropdown-menu">
                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('get-multiple-1'))">Multiple requests</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('get-path'))">Path fuzzing</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('get-path-qs'))">Querystring fuzzing</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('get-discovery-path-qs'))">Discovery directories & files</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('get-path-mutate-1'))">Path param mutation</a>
                  </li>

                  <li><a class="dropdown-item" href="#" 
                  @click="(loadExample('get-with-random-qs-1'))">Querystring param ramdomized values</a>
                  </li>
                </ul>
              </div>
            </div>

            <!--post-->
            <div class="col">
              <div class="btn-group">
                  <button type="button" class="btn btn-info btn-sm dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                    POST
                  </button>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#" 
                      @click="(loadExample('post-json'))">JSON body</a>
                    </li>

                    <li><a class="dropdown-item" href="#" 
                      @click="(loadExample('post-xml'))">XML body</a>
                    </li>

                    <li><a class="dropdown-item" href="#" 
                      @click="(loadExample('post-html-xss'))">HTML body</a>
                    </li>

                    <li><a class="dropdown-item" href="#" 
                      @click="(loadExample('post-xwwwformurlencoded'))">x-www-form-urlencoded</a>
                    </li>
                  </ul>
              </div>
            </div>

            <div class="col">
              <div class="btn-group">
                  <button type="button" class="btn btn-info btn-sm dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                    Upload file
                  </button>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#" 
                      @click="(loadExample('post-file'))">file with naughty content</a>
                    </li>

                    <li><a class="dropdown-item" href="#" 
                      @click="(loadExample('post-pdf'))">PDF</a>
                    </li>

                    <li><a class="dropdown-item" href="#" 
                      @click="(loadExample('post-image'))">Image</a>
                    </li>

                    <li><a class="dropdown-item" href="#"
                      @click="(loadExample('file-upload-myfile-batchfile'))">custom file content - delimited batch-file</a>
                    </li>

                    <li><a class="dropdown-item" href="#"
                      @click="(loadExample('file-upload-myfile-json'))">custom file content - JSON</a>
                    </li>

                    <li><a class="dropdown-item" href="#"
                      @click="(loadExample('file-upload-myfile-wordlisttypes'))">custom file content - primitive wordlist-type support</a>
                    </li>
                  </ul>
              </div>
            </div>
            
            <div class="col">
              <div class="btn-group">
                <button type="button" class="btn btn-info btn-sm dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                  GraphQL
                </button>
                <ul class="dropdown-menu">
                  
                  <li><a class="dropdown-item" href="#"
                    @click="(loadExample('gql-query-1'))">Query with param</a>
                  </li>

                  <li><a class="dropdown-item" href="#"
                    @click="(loadExample('gql-mutation-mutate-var-1'))">Mutate with Variables</a>
                  </li>

                </ul>
              </div>
            </div>

            <div class="col">
              <div class="btn-group">
                <button type="button" class="btn btn-info btn-sm dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                  MISC
                </button>
                <ul class="dropdown-menu">
                  
                  <li><a class="dropdown-item" href="#"
                    @click="(loadExample('misc-mutate-post'))">Mutate your input</a>
                  </li>

                  <li><a class="dropdown-item" href="#"
                    @click="(loadExample('misc-http-port-scan'))">HTTP port scanning</a>
                  </li>

                  <li><a class="dropdown-item" href="#"
                    @click="(loadExample('misc-variables-1'))">Global variables</a>
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