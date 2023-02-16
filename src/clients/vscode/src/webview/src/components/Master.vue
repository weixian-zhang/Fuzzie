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
  import { inject } from 'vue';
  import { Options, Vue } from 'vue-class-component';
  import ApiDiscovery from './ApiDiscovery.vue';
  import FuzzCaseSetPanel from './FuzzCaseSetPanel.vue';
  import FuzzResultPanel from './FuzzResultPanel.vue';
  import EventEmitter from 'eventemitter3'
  import Toast from 'primevue/toast';
  import { useToast } from "primevue/usetoast";
  import Splitter from 'primevue/splitter';
  import SplitterPanel from 'primevue/splitterpanel';
  import {FuzzerStatus, WebApiFuzzerInfo} from '../Model'; 
  import FuzzerWebClient from "../services/FuzzerWebClient";
  import FuzzerManager from "../services/FuzzerManager";
  import Logger from "../Logger";

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
    wc = new FuzzerWebClient()
    fm = new FuzzerManager(this.wc);
    toast = useToast();
    fuzzerConnected = false;
    $logger;
    isFuzzInProgress = false;


    public beforeMount() {

      this.$logger = inject('$logger'); 

      this.$logger.info('Webview - initializing Master pane and sub-panes');

      this.wc.subscribeWS('event.info', this.onEventInfo);
      this.wc.subscribeWS('event.error', this.onEventError);

      this.wc.subscribeWS('fuzz.update.casesetrunsummary', this.onUpdateCaseSetRunSummary);
      this.wc.subscribeWS('fuzz.update.fuzzdatacase', this.onNewFuzzDataCase);
    }

    public mounted() {

      this.toastInfo('trying to connect to fuzzer');

      this.wc.connectWS();

      setInterval(this.checkFuzzerReady, 1500);
    }

    
    async checkFuzzerReady(): Promise<void> {

      const status: FuzzerStatus|undefined = await this.wc.isFuzzerReady();

         if(status == undefined) {
            //stop any fuzzing activity
            this.fuzzerConnected = false;
            this.notifyFuzzerIsNotReady();
            this.toastInfo('fuzzer engine starting up, can take up to 15 secs on first launch', '', 1500);
            return;
         }

        if(status.webapiFuzzerInfo.isFuzzing) {
          this.isFuzzInProgress = true;
          this.eventemitter.emit('fuzz.start', status.webapiFuzzerInfo);
        }
        //fuzzing status from server says fuzzing stopped, while local tracking variable is true.
        // this means fuzzing just stopped
        else if (status.webapiFuzzerInfo.isFuzzing == false && this.isFuzzInProgress == true) {
            this.isFuzzInProgress = false;
            this.eventemitter.emit('fuzz.stop');
        }

         if (!status.isDataLoaded) {
            this.toastInfo('connected to fuzzer at http://localhost:50001, loading data...', '', 3000)
            return;
         } else {
            if(!this.fuzzerConnected) {
              this.notifyFuzzerReady();
              this.toastSuccess('fuzzer is ready at http://localhost:50001');
              this.fuzzerConnected = true;
            }
         }
    }


    private onEventInfo(msg: string) {
      this.$logger.info(msg);
    }

    private onEventError(errorMsg: string) {
      this.$logger.errorMsg(errorMsg);
    }

    private notifyFuzzerIsNotReady() {
        this.$logger.info('fuzzer is not ready, trying to reconnect. Fuzzer may take a while to load for the first time')
        this.eventemitter.emit('fuzzer.notready')
    }

    private notifyFuzzerReady() {
        this.$logger.info('fuzzer is ready');
        this.eventemitter.emit('fuzzer.ready')
    }

    private onUpdateCaseSetRunSummary(data) {
      this.eventemitter.emit('fuzz.update.casesetrunsummary', data)
    }

    private onNewFuzzDataCase(data) {
      this.eventemitter.emit('fuzz.update.fuzzdatacase', data)
    }
    
    toastInfo (msg: string, title = '', duration=2000)  {
        this.$toast.add({severity:'info', summary: title, detail: msg, life: duration});
    }

    toastError (msg: string, title = '', duration=4000)  {
        this.$toast.add({severity:'error', summary: title, detail: msg, life: duration});
    }

    toastSuccess (msg: string, title = '', duration=1000) {
        this.$toast.add({severity:'success', summary: title, detail: msg, life: duration});
    }
  }
  
  </script>

<style>

html {
  overflow: scroll !important;
}

</style>