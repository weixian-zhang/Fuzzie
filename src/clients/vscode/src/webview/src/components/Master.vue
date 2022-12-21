<template>
  <div class="container-fluid h-100 d-flex flex-column">
    <Toast />
    <Splitter style="height: 100%" >
      <SplitterPanel :size="100">
        <Splitter layout="vertical" gutterSize="0" >
          <SplitterPanel :size="40" >
            <Splitter gutterSize="8" >
              <SplitterPanel class="flex align-items-center justify-content-center" :size="25" >
                <ApiDiscovery
                  :toastInfo="toastInfo" 
                  :toastError="toastError"
                  :toastSuccess="toastSuccess"
                  :vscodeMsger="vscodeMsger" 
                  :eventemitter="eventemitter" 
                  :fuzzermanager="fm" 
                  :webclient="wc" />
              </SplitterPanel>
              <SplitterPanel class="flex align-items-center justify-content-center" :size="75">
                <FuzzCaseSetPanel :toast="toast" 
                   :toastInfo="toastInfo" 
                   :toastError="toastError"
                   :toastSuccess="toastSuccess"
                   :eventemitter="eventemitter" 
                   :fuzzermanager="fm" 
                   :webclient="wc" />
              </SplitterPanel>
            </Splitter>
          </SplitterPanel>

          <SplitterPanel class="flex align-items-center justify-content-center" :size="60" mt="3" >
            <FuzzResultPanel  :toast="toast"  
              :toastInfo="toastInfo" 
              :toastError="toastError"
              :toastSuccess="toastSuccess"
              :eventemitter="eventemitter" 
              :fuzzermanager="fm" 
              :webclient="wc" />
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
  import {FuzzerStatus} from '../Model'; 
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

    eventemitter = new EventEmitter();
    vscodeMsger = new VSCodeMessager();
    wc = new FuzzerWebClient()
    fm = new FuzzerManager(this.wc);
    toast = useToast();
    fuzzerConnected = false;

    public beforeMount() {

      this.wc.subscribeWS('event.info', this.sendEventToVSCodeConsole);
      this.wc.subscribeWS('event.error', this.sendEventToVSCodeConsole);

      this.wc.subscribeWS('fuzz.start', this.onFuzzStart);
      this.wc.subscribeWS('fuzz.complete', this.onFuzzComplete);
      this.wc.subscribeWS('fuzz.cancel', this.onFuzzCancel);

      this.wc.subscribeWS('fuzz.update.casesetrunsummary', this.onUpdateCaseSetRunSummary);
      this.wc.subscribeWS('fuzz.update.fuzzdatacase', this.onNewFuzzDataCase);
    }

    public mounted() {

      this.toastInfo('trying to connect to fuzzer');

      this.wc.connectWS();

      setInterval(this.checkFuzzerReady, 4000);
    }

    
    async checkFuzzerReady(): Promise<void> {
      const [ok, err, result] = await this.fm.isFuzzerReady();

         if(!ok) {
            //stop any fuzzing activity
            this.fuzzerConnected = false;
            this.notifyFuzzerIsNotReady();
            this.toastError('fuzzer is not ready, retrying...', '', 1000);
            return;
         }

         if (!result.isDataLoaded) {
            this.toastInfo('connected to fuzzer, loading corpora, this may take a moment')
            return;
         } else {
            if(!this.fuzzerConnected) {
              this.notifyFuzzerReady();
              this.toastSuccess('fuzzer is ready');
              this.fuzzerConnected = true;
            }
         }
    }


    private sendEventToVSCodeConsole(msg: string) {
      this.vscodeMsger.send(msg);
    }

    private notifyFuzzerIsNotReady() {
         this.eventemitter.emit('fuzzer.notready')
    }

    private notifyFuzzerReady() {
         this.eventemitter.emit('fuzzer.ready')
    }

    // data schema: {'fuzzCaseSetRunId': '', 'fuzzcontextId': ''}
    private onFuzzStart(data) {
      this.eventemitter.emit('fuzz.start', data);
    }

    private onFuzzComplete(data) {
      this.eventemitter.emit('fuzz.complete')
    }

    private onFuzzCancel(data) {
      this.eventemitter.emit('fuzz.cancel')
    }

    private onUpdateCaseSetRunSummary(data) {
      this.eventemitter.emit('fuzz.update.casesetrunsummary')
    }

    private onNewFuzzDataCase(data) {
      
      this.eventemitter.emit('fuzz.update.fuzzdatacase')
    }
    
    toastInfo (msg: string, title = '', duration=4000)  {
        this.$toast.add({severity:'info', summary: title, detail: msg, life: duration});
    }

    toastError (msg: string, title = '', duration=4000)  {
        this.$toast.add({severity:'error', summary: title, detail: msg, life: duration});
    }

    toastSuccess (msg: string, title = '', duration=4000) {
        this.$toast.add({severity:'success', summary: title, detail: msg, life: duration});
    }
  }
  
  </script>

<style>

html {
  overflow: scroll !important;
}

</style>