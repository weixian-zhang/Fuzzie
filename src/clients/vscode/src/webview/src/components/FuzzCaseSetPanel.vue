
<!-- https://primefaces.org/primevue/treetable/responsive -->

<template>
  <v-card
  color="white"
  outlined
  width="100%"
  height="100%">
    <v-toolbar card color="cyan" flat dense height="50px">
      <v-spacer />
      <!-- <v-btn icon height="30px" width="30px">
        <v-icon :disabled="!isFuzzcontextsGetComplete" @click="getFuzzcontexts">mdi-refresh</v-icon>
      </v-btn> -->
      <v-btn icon height="30px" width="30px">
        <v-icon >mdi-card-plus</v-icon>
      </v-btn>
    </v-toolbar>
    <div v-show="showTable">
      <TreeTable :value="nodes" class="p-treetable-sm" style="margin-bottom: 2rem" :scrollable="true" scroll-height="400px" :resizableColumns="true" columnResizeMode="fit" showGridlines>
        <Column field="verb" header="Verb">
        </Column>
        <Column field="path" header="Path"></Column>
        <Column field="http2xx" header="2xx"></Column>
        <Column field="http3xx" header="Type"></Column>
        <Column field="" header="Body"  :expander="true">
          <template #header>
            children: 
          </template>
          <template #body="slotProps">
            
            {{ slotProps.node.data.body }}
          </template>
        </Column>
    </TreeTable>
      </div>
  </v-card>
  
</template>
      
 
    
 <script>

import TreeTable  from 'primevue/treetable';
import Column from 'primevue/column';
import { Options, Vue } from 'vue-class-component';

@Options({
  components: {
    TreeTable,
    Column
  },
  props: {
    // msg: String
  }
})

 export default class FuzzCaseSetPanel extends Vue {

  
  nodes  = [
      {
        key:"0",
        data: {
          verb:"POST",
          path:"100kb",
          http2xx:"Folder"
        },
        children:[{
            key:"0-0",
            data: {
              body: "I am the body",
              others: "others of course"
            }
            
           
          }]
          
          
      }
  ];
  
  // [
  //       {"key":"0","data":{"name":"Applications","size":"100kb","type":"Folder"},
  //       "children":[{"key":"0-0","data":{"body":"sdasadadad"},
  //       "children":[{"key":"0-0-0","data":{"name":"vue.app","size":"10kb","type":"Application"}},{"key":"0-0-1","data":{"name":"native.app","size":"10kb","type":"Application"}},{"key":"0-0-2","data":{"name":"mobile.app","size":"5kb","type":"Application"}}]},{"key":"0-1","data":{"name":"editor.app","size":"25kb","type":"Application"}},{"key":"0-2","data":{"name":"settings.app","size":"50kb","type":"Application"}}]},
  //       {"key":"1","data":{"name":"Cloud","size":"20kb","type":"Folder"},"children":[{"key":"1-0","data":{"name":"backup-1.zip","size":"10kb","type":"Zip"}},{"key":"1-1","data":{"name":"backup-2.zip","size":"10kb","type":"Zip"}}]},
  //       {"key":"2","data":{"name":"Desktop","size":"150kb","type":"Folder"},"children":[{"key":"2-0","data":{"name":"note-meeting.txt","size":"50kb","type":"Text"}},{"key":"2-1","data":{"name":"note-todo.txt","size":"100kb","type":"Text"}}]},
  //       {"key":"3","data":{"name":"Documents","size":"75kb","type":"Folder"},"children":[{"key":"3-0","data":{"name":"Work","size":"55kb","type":"Folder"},"children":[{"key":"3-0-0","data":{"name":"Expenses.doc","size":"30kb","type":"Document"}},{"key":"3-0-1","data":{"name":"Resume.doc","size":"25kb","type":"Resume"}}]},{"key":"3-1","data":{"name":"Home","size":"20kb","type":"Folder"},"children":[{"key":"3-1-0","data":{"name":"Invoices","size":"20kb","type":"Text"}}]}]},
  //       {"key":"4","data":{"name":"Downloads","size":"25kb","type":"Folder"},"children":[{"key":"4-0","data":{"name":"Spanish","size":"10kb","type":"Folder"},"children":[{"key":"4-0-0","data":{"name":"tutorial-a1.txt","size":"5kb","type":"Text"}},{"key":"4-0-1","data":{"name":"tutorial-a2.txt","size":"5kb","type":"Text"}}]},{"key":"4-1","data":{"name":"Travel","size":"15kb","type":"Text"},"children":[{"key":"4-1-0","data":{"name":"Hotel.pdf","size":"10kb","type":"PDF"}},{"key":"4-1-1","data":{"name":"Flight.pdf","size":"5kb","type":"PDF"}}]}]},
  //       {"key":"5","data":{"name":"Main","size":"50kb","type":"Folder"},"children":[{"key":"5-0","data":{"name":"bin","size":"50kb","type":"Link"}},{"key":"5-1","data":{"name":"etc","size":"100kb","type":"Link"}},{"key":"5-2","data":{"name":"var","size":"100kb","type":"Link"}}]},
  //       {"key":"6","data":{"name":"Other","size":"5kb","type":"Folder"},"children":[{"key":"6-0","data":{"name":"todo.txt","size":"3kb","type":"Text"}},{"key":"6-1","data":{"name":"logo.png","size":"2kb","type":"Picture"}}]},
  //       {"key":"7","data":{"name":"Pictures","size":"150kb","type":"Folder"},"children":[{"key":"7-0","data":{"name":"barcelona.jpg","size":"90kb","type":"Picture"}},{"key":"7-1","data":{"name":"primeng.png","size":"30kb","type":"Picture"}},{"key":"7-2","data":{"name":"prime.jpg","size":"30kb","type":"Picture"}}]},
  //       {"key":"8","data":{"name":"Videos","size":"1500kb","type":"Folder"},"children":[{"key":"8-0","data":{"name":"primefaces.mkv","size":"1000kb","type":"Video"}},{"key":"8-1","data":{"name":"intro.avi","size":"500kb","type":"Video"}}]}
  //   ]
 
  columns = [
            {field: 'name', header: 'Vin', expander: true},
            {field: 'size', header: 'Size'},
            {field: 'type', header: 'Type'}
        ];

  showTable = this.nodes.length > 0 ? "true": "false";

 }
 
 </script>
 
 <!-- Add "scoped" attribute to limit CSS to this component only -->
 <style scoped>

.v-card {
  display: flex !important;
  flex-direction: column;
}

.v-card__text {
  flex-grow: 1;
  overflow: auto;
}

 </style>
 