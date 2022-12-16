<template>
  <div class="container-fluid h-100 d-flex flex-column">
    <Toast />
    <Splitter style="height: 100%" >
      <SplitterPanel :size="100">
        <Splitter layout="vertical" gutterSize="0" >
          <SplitterPanel :size="40" >
            <Splitter gutterSize="8" >
              <SplitterPanel class="flex align-items-center justify-content-center" :size="25" >
                <ApiDiscovery :toast="toast" :vscodeMsger="vscodeMsger" :eventemitter="eventemitter" :fuzzermanager="fm" :webclient="wc" />
              </SplitterPanel>
              <SplitterPanel class="flex align-items-center justify-content-center" :size="75">
                <FuzzCaseSetPanel :toast="toast"  :eventemitter="eventemitter" :fuzzermanager="fm" :webclient="wc" />
              </SplitterPanel>
            </Splitter>
          </SplitterPanel>

          <SplitterPanel class="flex align-items-center justify-content-center" :size="60" mt="3" >
            <FuzzResultPanel  :toast="toast"  :eventemitter="eventemitter" :fuzzermanager="fm" :webclient="wc" />
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
  import { useToast } from "primevue/usetoast";
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
    private toast = useToast();

    public beforeMount() {

      this.wc.subscribeWS('event.info', this.sendEventToVSCodeConsole);
      this.wc.subscribeWS('event.error', this.sendEventToVSCodeConsole);

      this.wc.subscribeWS('fuzz.start', this.notifyFuzzStart);
      this.wc.subscribeWS('fuzz.complete', this.notifyFuzzComplete);
      this.wc.subscribeWS('fuzz.cancel', this.notifyFuzzCancel);

      this.wc.subscribeWS('fuzz.update.casesetrunsummary', this.notifyUpdateCaseSetRunSummary);
      this.wc.subscribeWS('fuzz.update.fuzzdatacase', this.notifyUpdateCaseSetRunSummary);

      // self.eventstore.feedback_client('fuzz.update.casesetrunsummary', summaryViewModel)
      //       self.eventstore.feedback_client('', fuzzDataCase)
    }

    public mounted() {
     
      this.wc.connectWSServer()
    }

    private sendEventToVSCodeConsole(msg: string) {
      this.vscodeMsger.send(msg);
    }

    // data schema: {'fuzzCaseSetRunId': '', 'fuzzcontextId': ''}
    private notifyFuzzStart(data) {
      this.eventemitter.emit('fuzz.start')
    }

    private notifyFuzzComplete(data) {
      this.eventemitter.emit('fuzz.complete')
    }

    private notifyFuzzCancel(data) {
      this.eventemitter.emit('fuzz.cancel')
    }

    private notifyUpdateCaseSetRunSummary(data) {
      this.eventemitter.emit('fuzz.update.casesetrunsummary')
    }
  }
  

  </script>

<style>

html {
  overflow: scroll !important;
}

</style>