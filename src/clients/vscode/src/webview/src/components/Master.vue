<template>
    
    <div class="container-fluid h-100 d-flex flex-column">
      <Toast />
      
        <div class="row h-50" >
          <Splitter>
            <SplitterPanel class="col-3">
              <div >
                  <ApiDiscovery :vscodeMsger="vscodeMsger" :eventemitter="eventemitter" />
              </div>
            </SplitterPanel>
            <SplitterPanel class="col-9">
              <div >
                  <FuzzCaseSetPanel  :eventemitter="eventemitter" />
              </div>
            </SplitterPanel>
            <div class="row flex-fill d-flex">
              <SplitterPanel >
               <Splitter  layout="vertical">
                 <SplitterPanel  >
                    <FuzzResultPanel />
                 </SplitterPanel>
               </Splitter>
              </SplitterPanel>
            </div>
            
           
          </Splitter>
          
        </div>
        
    </div>
</template>
  
<script lang="ts">
  import { Options, Vue } from 'vue-class-component';
  import ApiDiscovery from './ApiDiscovery.vue';
  import FuzzCaseSetPanel from './FuzzCaseSetPanel.vue';
  import FuzzResultPanel from './FuzzResultPanel.vue';
  import EventEmitter from 'eventemitter3'
  import VSCodeMessager from '../services/VSCodeMessager';
  import Toast from 'primevue/toast';
  import Splitter from 'primevue/splitter';
  import SplitterPanel from 'primevue/splitterpanel';

  @Options({
    components: {
      ApiDiscovery,
      FuzzCaseSetPanel,
      FuzzResultPanel,
      Toast,
      Splitter,
      SplitterPanel
    },
  })
  export default class Master extends Vue {

    eventemitter = new EventEmitter();

    vscodeMsger = new VSCodeMessager();

  }
  </script>

<style>

html {
  overflow: scroll !important;
}

</style>