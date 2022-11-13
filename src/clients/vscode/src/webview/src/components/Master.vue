<template>
    <div class="container-fluid d-flex h-100 flex-column">
        <div class="row h-50 mt-1">
            <div class="col-3">
                <ApiDiscovery :vscodeMsger="vscodeMsger" :eventemitter="eventemitter" />
            </div>
            <div class="col-9">
                <FuzzCaseSetPanel  :eventemitter="eventemitter" />
            </div>
        </div>

        <div class="row flex-fill d-flex  mt-2 mb-0">
            <FuzzResultPanel />
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

  @Options({
    components: {
      ApiDiscovery,
      FuzzCaseSetPanel,
      FuzzResultPanel
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