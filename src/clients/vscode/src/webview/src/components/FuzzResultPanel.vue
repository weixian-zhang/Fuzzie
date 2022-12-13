<template>
    <v-card
      color="white"
      outlined>

     <v-toolbar color="cyan" flat dense height="50px">
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

<!-- {
    "timestamp": "2022-12-13T14:26:05.561685",
    "data": {
        "fuzzCaseSetId": "iRz6x5XGX7rLnUefain4ND",
        "fuzzCaseSetRunId": null,
        "fuzzcontextId": "RmX6YSbjworA2dZjFmhqAi",
        "selected": null,
        "verb": null,
        "path": null,
        "querystringNonTemplate": null,
        "bodyNonTemplate": null,
        "headerNonTemplate": null,
        "authnType": null,
        "file": null,
        "runSummaryId": null,
        "http2xx": 0,
        "http3xx": 0,
        "http4xx": 49,
        "http5xx": 0,
        "completedDataCaseRuns": 49,
        "Id": "GyAcvFtNGzmFJB5NKByXdc"
    },
    "topic": "fuzz.case_set_run_summary"
} -->

  <!-- {
    "timestamp": "2022-12-13T14:26:05.569780",
    "data": {
        "Id": "fuYWTs9MTGxTSKhPRA4Fzo",
        "fuzzCaseSetId": "iRz6x5XGX7rLnUefain4ND",
        "fuzzCaseSetRunId": "",
        "fuzzcontextId": "RmX6YSbjworA2dZjFmhqAi",
        "request": {
            "Id": "DDFxt4AJjNtYVoFN59tgkV",
            "fuzzDataCaseId": "fuYWTs9MTGxTSKhPRA4Fzo",
            "fuzzcontextId": "RmX6YSbjworA2dZjFmhqAi",
            "hostnamePort": "https://httpbin.org:443",
            "verb": "GET",
            "path": "/when/\"%s%p%x%d * 513\"",
            "querystring": "",
            "url": "https://httpbin.org:443/when/\"%s%p%x%d * 513\"",
            "headers": "{}",
            "body": "{}",
            "requestMessage": "\n            GET /when/\"%s%p%x%d * 513\" HTTP/1.1\n            \n\n            \n            ",
            "contentLength": "4",
            "datetime": "2022-12-13T14:26:03.833164"
        },
        "response": {
            "fuzzDataCaseId": "fuYWTs9MTGxTSKhPRA4Fzo",
            "fuzzcontextId": "RmX6YSbjworA2dZjFmhqAi",
            "statusCode": 404,
            "reasonPharse": "NOT FOUND",
            "responseDisplayText": "\n        \n    HTTP/1.1 404 NOT FOUND\n        Date: Tue, 13 Dec 2022 06:26:00 GMT\nContent-Type: text/html\nContent-Length: 233\nConnection: keep-alive\nServer: gunicorn/19.9.0\nAccess-Control-Allow-Origin: *\nAccess-Control-Allow-Credentials: true\n\n              \n        <!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>\n\n        ",
            "headerJson": "",
            "setcookieHeader": "",
            "body": "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>\n",
            "contentLength": "233",
            "Id": "AkqUyM2swmwYisXKchmHNY",
            "datetime": "2022-12-13T14:26:05.188108",
            "headersJson": "{\"Date\": \"Tue, 13 Dec 2022 06:26:00 GMT\", \"Content-Type\": \"text/html\", \"Content-Length\": \"233\", \"Connection\": \"keep-alive\", \"Server\": \"gunicorn/19.9.0\", \"Access-Control-Allow-Origin\": \"*\", \"Access-Control-Allow-Credentials\": \"true\"}"
        }
    },
    "topic": "fuzz.fuzzdatacase"
} -->
 }
 
 </script>
 
 <!-- Add "scoped" attribute to limit CSS to this component only -->
 <style scoped>

 </style>
 