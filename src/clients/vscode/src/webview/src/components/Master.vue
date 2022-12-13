<template>
  <div class="container-fluid h-100 d-flex flex-column">
    <Toast />
    <Splitter style="height: 100%" >
      <SplitterPanel :size="100">
        <Splitter layout="vertical" gutterSize="5">
          <SplitterPanel :size="40" >
            <Splitter gutterSize="5">
              <SplitterPanel class="flex align-items-center justify-content-center" :size="25" >
                <ApiDiscovery :vscodeMsger="vscodeMsger" :eventemitter="eventemitter" />
              </SplitterPanel>
              <SplitterPanel class="flex align-items-center justify-content-center" :size="75">
                <FuzzCaseSetPanel  :eventemitter="eventemitter" />
              </SplitterPanel>
            </Splitter>
          </SplitterPanel>
          <SplitterPanel class="flex align-items-center justify-content-center" :size="60" mt="3">
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