<template>
    <v-card
     width="100%"
     height="100%">

     <v-toolbar color="blue" dense flat="true" height="50px">
      <v-spacer />
      <v-btn icon height="30px" width="30px">
        <v-icon>mdi-card-plus</v-icon>
      </v-btn>
    </v-toolbar>
   </v-card>
 
      
 </template>
 
 <script>

import { Options, Vue } from 'vue-class-component';
@Options({
  props: {
    // msg: String
  }
})

 export default class FuzzResultPanel extends Vue {
 }
 
 </script>
 
 <!-- Add "scoped" attribute to limit CSS to this component only -->
 <style scoped>

 </style>
 