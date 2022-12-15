<template>
  <div class="container-fluid h-100 d-flex flex-column">
    <Toast />
    <Splitter style="height: 100%" >
      <SplitterPanel :size="100">
        <Splitter layout="vertical" gutterSize="0" >
          <SplitterPanel :size="40" >
            <Splitter gutterSize="8" >
              <SplitterPanel class="flex align-items-center justify-content-center" :size="30" >
                <ApiDiscovery :vscodeMsger="vscodeMsger" :eventemitter="eventemitter" :fuzzermanager="fm" :webclient="wc" />
              </SplitterPanel>
              <SplitterPanel class="flex align-items-center justify-content-center" :size="70">
                <FuzzCaseSetPanel  :eventemitter="eventemitter" :fuzzermanager="fm" :webclient="wc" />
              </SplitterPanel>
            </Splitter>
          </SplitterPanel>

          <SplitterPanel class="flex align-items-center justify-content-center" :size="60" mt="3" >
            <FuzzResultPanel />
          </SplitterPanel>
        </Splitter>
      </SplitterPanel>
    </Splitter>
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

  import FuzzerWebClient from "../services/FuzzerWebClient";
  import FuzzerManager from "../services/FuzzerManager";

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

    private eventemitter = new EventEmitter();
    private vscodeMsger = new VSCodeMessager();
    private wc = new FuzzerWebClient()
    private fm = new FuzzerManager(this.wc);

    public beforeMount() {

      this.wc.subscribeWS('event.info', this.sendEventToVSCodeConsole);
      this.wc.subscribeWS('event.error', this.sendEventToVSCodeConsole);
    }

    public mounted() {
     
      this.wc.connectWSServer()
    }

    private sendEventToVSCodeConsole(msg: string) {
      this.vscodeMsger.send(msg);
    }

  }
  

  </script>

<style>

html {
  overflow: scroll !important;
}

</style>