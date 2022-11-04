<!-- https://pictogrammers.github.io/@mdi/font/6.9.96/ -->

<template>
  <v-card
  color="white"
  outlined
  width="100%"
  height="100%">
    <v-toolbar card color="blue" flat="true" dense height="50px">
      <v-spacer />
      <v-btn icon height="30px" width="30px">
        <v-icon :disabled="!isFuzzcontextsGetComplete" @click="getFuzzcontexts">mdi-refresh</v-icon>
      </v-btn>
      <v-btn icon height="30px" width="30px">
        <v-icon >mdi-card-plus</v-icon>
      </v-btn>
    </v-toolbar>
    <v-card-text >
      <Tree :value="fuzzcontexts" :expandedKeys="expandedKeys"></Tree>
    </v-card-text>
  </v-card>
  

</template>

<script>

import { Options, Vue } from 'vue-class-component';
import FuzzerManager from '@/services/FuzzerManager';
// import Tree from "vue3-tree";
// import "vue3-tree/dist/style.css";
import Tree from 'primevue/tree';

@Options({
  components: {
    Tree
  },
  props: {
    // msg: String
  }
})
export default class ApiDiscovery extends Vue {

  fm = new FuzzerManager();

  isFuzzcontextsGetComplete = true;
  expandedKeys= {"children": true};
  fuzzcontexts = [
        {
            "key": "0",
            "label": "Documents",
            "data": "Documents Folder",
            "icon": "pi pi-fw pi-inbox",
            "children": [{
                "key": "0-0",
                "label": "Work",
                "data": "Work Folder",
                "icon": "pi pi-fw pi-cog",
                "children": [{ "key": "0-0-0", "label": "Expenses.doc", "icon": "pi pi-fw pi-file", "data": "Expenses Document" }, { "key": "0-0-1", "label": "Resume.doc", "icon": "pi pi-fw pi-file", "data": "Resume Document" }]
            },
            {
                "key": "0-1",
                "label": "Home",
                "data": "Home Folder",
                "icon": "pi pi-fw pi-home",
                "children": [{ "key": "0-1-0", "label": "Invoices.txt", "icon": "pi pi-fw pi-file", "data": "Invoices for this month" }]
            }]
        },
        {
            "key": "1",
            "label": "Events",
            "data": "Events Folder",
            "icon": "pi pi-fw pi-calendar",
            "children": [
                { "key": "1-0", "label": "Meeting", "icon": "pi pi-fw pi-calendar-plus", "data": "Meeting" },
                { "key": "1-1", "label": "Product Launch", "icon": "pi pi-fw pi-calendar-plus", "data": "Product Launch" },
                { "key": "1-2", "label": "Report Review", "icon": "pi pi-fw pi-calendar-plus", "data": "Report Review" }]
        },
        {
            "key": "2",
            "label": "Movies",
            "data": "Movies Folder",
            "icon": "pi pi-fw pi-star",
            "children": [{
                "key": "2-0",
                "icon": "pi pi-fw pi-star",
                "label": "Al Pacino",
                "data": "Pacino Movies",
                "children": [{ "key": "2-0-0", "label": "Scarface", "icon": "pi pi-fw pi-video", "data": "Scarface Movie" }, { "key": "2-0-1", "label": "Serpico", "icon": "pi pi-fw pi-video", "data": "Serpico Movie" }]
            },
            {
                "key": "2-1",
                "label": "Robert De Niro",
                "icon": "pi pi-fw pi-star",
                "data": "De Niro Movies",
                "children": [{ "key": "2-1-0", "label": "Goodfellas", "icon": "pi pi-fw pi-video", "data": "Goodfellas Movie" }, { "key": "2-1-1", "label": "Untouchables", "icon": "pi pi-fw pi-video", "data": "Untouchables Movie" }]
            }]
        }
    ]
    //[
  //     {
  //       id: 1,
  //       label: "Animal",
  //       nodes: [
  //         {
  //           id: 2,
  //           label: "Dog",
  //         },
  //         {
  //           id: 3,
  //           label: "Cat",
  //           nodes: [
  //             {
  //               id: 4,
  //               label: "Egyptian Mau Cat",
  //             },
  //             {
  //               id: 5,
  //               label: "Japanese Bobtail Cat",
  //             },
  //           ],
  //         },
  //         {
  //           id: 6,
  //           label: "Cat",
  //           nodes: [
  //             {
  //               id: 7,
  //               label: "Egyptian Mau Cat",
  //             },
  //             {
  //               id: 8,
  //               label: "Japanese Bobtail Cat",
  //             },
  //           ],
  //         },
  //       ],
  //     },
  //     {
  //       id: 6,
  //       label: "People",
  //     },
  //   ]

  mounted() {
    this.getFuzzcontexts()
  }

  
  async getFuzzcontexts() {
    this.isFuzzcontextsGetComplete = false;
    const fcs = await this.fm.getFuzzcontexts()
    //this.fuzzcontexts = fcs;
    this.isFuzzcontextsGetComplete = true;
  }

  onTreeNodeClick = (node) => {
      console.log(node);
    };
}
</script>


<style scoped>
html {
  overflow: hidden !important;
}

.v-card {
  display: flex !important;
  flex-direction: column;
}

.v-card__text {
  flex-grow: 1;
  overflow: auto;
}
</style>
