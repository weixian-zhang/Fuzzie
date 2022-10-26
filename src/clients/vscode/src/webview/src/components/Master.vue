<template>
    <div class="container-fluid d-flex h-100 flex-column">
        <div class="row h-50">
            <div class="col">
                    <div class="card h-100 w-100">
                        <div class="card-header ">
                            <div class="container-fluid">
                                <div class="row ">
                                    <div class="col">
                                        Fuzz Contexts
                                    </div>
                                    <div class="col col-auto">
                                        <a href="#" class="btn btn-primary">Discover</a>
                                        
                                    </div>
                            
                                </div>
                            </div>
                        
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">Special title treatment</h5>
                            <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                        </div>
                    </div>
                </div>
                <div class="col-7">
                    <div class="card  h-100">
                        <div class="card-header">
                            <a href="#" class="btn btn-primary">Fuzz</a>
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">Special title treatment</h5>
                            <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                        </div>
                    </div>
                </div>
            
        </div>
        <div class="row flex-fill d-flex  mt-2 mb-3">
            <div class="card">
                    <div class="card-header">
                        Featured
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">Special title treatment</h5>
                        <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                        <a href="#" class="btn btn-primary">Go somewhere</a>
                    </div>
                </div>
        </div>
    </div>
</template>
  
  <script lang="ts">
  import { Options, Vue } from 'vue-class-component';
  
  @Options({
    components: {
      
    },
  })
  export default class Master extends Vue {}
  </script>