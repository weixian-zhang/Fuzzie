import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import "@mdi/font/css/materialdesignicons.css";
import { loadFonts } from './plugins/webfontloader'

import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/saga-blue/theme.css'      //theme
import 'primevue/resources/primevue.min.css'                //core css
import 'primeicons/primeicons.css'                         //icons
import ToastService from "primevue/toastservice";
import Tooltip from 'primevue/tooltip';

import 'jquery/dist/jquery.min.js';
import 'bootstrap';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';

import Logger from './Logger';

import {json} from "@codemirror/lang-json"
import { basicSetup } from 'codemirror'
import VueCodemirror from 'vue-codemirror'
import {EditorView, keymap} from "@codemirror/view"
import {CompletionContext, autocompletion} from "@codemirror/autocomplete"
import {indentWithTab,blockComment,blockUncomment} from "@codemirror/commands"

const logger = new Logger();

loadFonts()

const app = createApp(App);

app.provide("$logger", logger); // global singleton instance of logger

app.use(vuetify)
app.use(PrimeVue)
app.use(ToastService);

app.use(VueCodemirror, {
  // optional default global options
  autofocus: true,
  disabled: false,
  indentWithTab: true,
  tabSize: 2,
  //placeholder: 'Code goes here...',
  extensions:  [
    basicSetup, 
    json(),
    keymap.of([indentWithTab]),
    autocompletion({
      override: [function myCompletions(context: CompletionContext){

        const word = context.matchBefore(/\w*/)

        if (word != undefined && word.from == word.to && !context.explicit)
          return null;

          return {
            from: word ? word.from : context.pos,
            options: [
              {label: "bool", type: "keyword", apply: "{{ bool }}"},
              {label: "digit", type: "keyword", apply: "{{ digit }}", info: "digit or number range e.g: digit:1:5000.9999"},
              {label: "my", type: "keyword", apply: "{{ my:[your own input] }}", info: "or multiple custom input: {{my:[a quick brown fox],[Keep your head up]}}"},
              {label: "char", type: "keyword", apply: "{{ char }}"},
              {label: "image", type: "keyword", apply: "{{ image }}", info:"Images mix with other file types encode with 'latin1'"},
              {label: "pdf", type: "keyword", apply: "{{ pdf }}", info:"PDF mix with payload from danielmiessler seclist"},
              {label: "file", type: "keyword", apply: "{{ file }}", info:"danielmiessler's seclist payload encode with 'latin1'"},
              {label: "datetime", type: "keyword", apply: "{{ datetime }}", info:"date & time"},
              {label: "date", type: "keyword", apply: "{{ date }}", info:"date only"},
              {label: "time", type: "keyword", apply: "{{ time }}", info:"time only"},
              {label: "username", type: "keyword", apply: "{{ username }}", info:"usernames from danielmiessler seclist"},
              {label: "password", type: "keyword", apply: "{{ password }}", info:"password from danielmiessler seclist"},
              {label: "filename", type: "keyword", apply: "{{ filename }}", info:""},
              {label: "string", type: "keyword", apply: "{{ string }}", info:"A mix of big-list-of-naughty strings, and  xss and sqlinjection strings from danielmiessle/seclist"},
              {label: "xss", type: "keyword", apply: "{{ xss }}", info:"cross site scripting strings from danielmiessler/seclist"},
              {label: "sqlinject", type: "keyword", apply: "{{ sqlinject }}", info:"sql inection strings from danielmiessler/seclist"},

              {label: "GET", type: "keyword", apply: "GET", info:"GET HTTP verb"},
              {label: "PUT", type: "keyword", apply: "PUT", info:"PUT HTTP verb"},
              {label: "POST", type: "keyword", apply: "POST", info:"POST verb"},
              {label: "DELETE", type: "keyword", apply: "DELETE", info:"DELETE verb"},
              {label: "PATCH", type: "keyword", apply: "PATCH", info:"PATCH verb"},

              {label: "http", type: "keyword", apply: "http://", info:""},
              {label: "https", type: "keyword", apply: "https://", info:""},

              {label: "Accept", type: "keyword", apply: "Accept: ", info:""},
              {label: "Accept-Charset", type: "keyword", apply: "Accept-Charset: ", info:""},
              {label: "Accept-Datetime", type: "keyword", apply: "Accept-Datetime: ", info:""},
              {label: "Accept-Encoding", type: "keyword", apply: "Accept-Encoding: ", info:""},
              {label: "Accept-Language", type: "keyword", apply: "Accept-Language: ", info:""},
              {label: "Access-Control-Request-Method", type: "keyword", apply: "Access-Control-Request-Method: ", info:""},
              {label: "Access-Control-Request-Headers", type: "keyword", apply: "Access-Control-Request-Headers: ", info:""},
              {label: "Authorization", type: "keyword", apply: "Authorization: ", info:""},
              {label: "Cache-Control", type: "keyword", apply: "Cache-Control: ", info:""},
              {label: "Connection", type: "keyword", apply: "Connection: ", info:""},
              {label: "Content-Encoding", type: "keyword", apply: "Content-Encoding: ", info:""},
              {label: "Content-Length", type: "keyword", apply: "Content-Length: ", info:""},
              {label: "Content-MD5", type: "keyword", apply: "Content-MD5: ", info:""},
              {label: "Content-Type", type: "keyword", apply: "Content-Type: ", info:""},
              {label: "Cookie", type: "keyword", apply: "Cookie: ", info:""},
              {label: "Date", type: "keyword", apply: "Date: ", info:""},
              {label: "Expect", type: "keyword", apply: "Expect: ", info:""},
              {label: "Forwarded", type: "keyword", apply: "Forwarded: ", info:""},
              {label: "From", type: "keyword", apply: "From: ", info:""},
              {label: "Host", type: "keyword", apply: "Host: ", info:""},
              {label: "HTTP2-Settings", type: "keyword", apply: "HTTP2-Settings: ", info:""},
              {label: "If-Match", type: "keyword", apply: "If-Match: ", info:""},
              {label: "If-Modified-Since", type: "keyword", apply: "If-Modified-Since: ", info:""},
              {label: "If-None-Match", type: "keyword", apply: "If-None-Match: ", info:""},
              {label: "If-Range", type: "keyword", apply: "If-Range: ", info:""},
              {label: "If-Unmodified-Since", type: "keyword", apply: "If-Unmodified-Since: ", info:""},
              {label: "Max-Forwards", type: "keyword", apply: "Max-Forwards: ", info:""},
              {label: "Origin", type: "keyword", apply: "Origin: ", info:""},
              {label: "Pragma", type: "keyword", apply: "Pragma: ", info:""},
              {label: "Prefer", type: "keyword", apply: "Prefer: ", info:""},
              {label: "Proxy-Authorization", type: "keyword", apply: "Proxy-Authorization: ", info:""},
              {label: "Range", type: "keyword", apply: "Range: ", info:""},
              {label: "Referer", type: "keyword", apply: "Referer: ", info:""},
              {label: "Trailer", type: "keyword", apply: "Trailer: ", info:""},
              {label: "Transfer-Encoding", type: "keyword", apply: "Transfer-Encoding: ", info:""},
              {label: "User-Agent", type: "keyword", apply: "User-Agent: ", info:""},
              {label: "Upgrade", type: "keyword", apply: "Upgrade: ", info:""},
              {label: "X-Requested-With", type: "keyword", apply: "X-Requested-With: ", info:""},
              {label: "X-Forwarded-For", type: "keyword", apply: "X-Forwarded-For: ", info:""},
              {label: "X-Forwarded-Host", type: "keyword", apply: "X-Forwarded-Host: ", info:""},
              {label: "X-Forwarded-Proto", type: "keyword", apply: "X-Forwarded-Proto: ", info:""},
              {label: "Front-End-Https", type: "keyword", apply: "Front-End-Https: ", info:""},
              {label: "X-Http-Method-Override", type: "keyword", apply: "X-Http-Method-Override: ", info:""},
              {label: "X-ATT-DeviceId", type: "keyword", apply: "X-ATT-DeviceId: ", info:""},
              {label: "X-Wap-Profile", type: "keyword", apply: "X-Wap-Profile: ", info:""},
              {label: "Proxy-Connection", type: "keyword", apply: "Proxy-Connection: ", info:""},
              {label: "X-UIDH", type: "keyword", apply: "X-UIDH: ", info:""},
              {label: "X-Csrf-Token", type: "keyword", apply: "X-Csrf-Token: ", info:""},
              {label: "X-Request-ID", type: "keyword", apply: "X-Request-ID: ", info:""},
              {label: "X-Correlation-ID ", type: "keyword", apply: "X-Correlation-ID : ", info:""},
              {label: "Correlation-ID", type: "keyword", apply: "Correlation-ID: ", info:""},


              {label: "application/java-archive", type: "keyword", apply: "application/java-archive", info:""},
              {label: "application/EDI-X12", type: "keyword", apply: "application/EDI-X12", info:""},
              {label: "application/EDIFACT", type: "keyword", apply: "application/EDIFACT", info:""},
              {label: "application/javascript", type: "keyword", apply: "application/javascript", info:""},
              {label: "application/octet-stream", type: "keyword", apply: "application/octet-stream", info:""},
              {label: "application/ogg", type: "keyword", apply: "application/ogg", info:""},
              {label: "application/pdf", type: "keyword", apply: "application/pdf", info:""},
              {label: "application/xhtml+xml", type: "keyword", apply: "application/xhtml+xml", info:""},
              {label: "application/x-shockwave-flash", type: "keyword", apply: "application/x-shockwave-flash", info:""},
              {label: "application/json", type: "keyword", apply: "application/json", info:""},
              {label: "application/ld+json", type: "keyword", apply: "application/ld+json", info:""},
              {label: "application/xml", type: "keyword", apply: "application/xml", info:""},
              {label: "application/zip", type: "keyword", apply: "application/zip", info:""},
              {label: "application/x-www-form-urlencoded", type: "keyword", apply: "application/x-www-form-urlencoded", info:""},
              {label: "audio/mpeg", type: "keyword", apply: "audio/mpeg", info:""},
              {label: "audio/x-ms-wma", type: "keyword", apply: "audio/x-ms-wma", info:""},
              {label: "audio/vnd.rn-realaudio", type: "keyword", apply: "audio/vnd.rn-realaudio", info:""},
              {label: "audio/x-wav", type: "keyword", apply: "audio/x-wav", info:""},
              {label: "image/gif", type: "keyword", apply: "image/gif", info:""},
              {label: "image/jpeg", type: "keyword", apply: "image/jpeg", info:""},
              {label: "image/png", type: "keyword", apply: "image/png", info:""},
              {label: "image/tiff", type: "keyword", apply: "image/tiff", info:""},
              {label: "image/vnd.microsoft.icon", type: "keyword", apply: "image/vnd.microsoft.icon", info:""},
              {label: "image/x-icon", type: "keyword", apply: "image/x-icon", info:""},
              {label: "image/vnd.djvu", type: "keyword", apply: "image/vnd.djvu", info:""},
              {label: "image/svg+xml", type: "keyword", apply: "image/svg+xml", info:""},
              {label: "multipart/mixed", type: "keyword", apply: "multipart/mixed", info:""},
              {label: "multipart/alternative", type: "keyword", apply: "multipart/alternative", info:""},
              {label: "multipart/related", type: "keyword", apply: "multipart/related", info:""},
              {label: "multipart/form-data", type: "keyword", apply: "multipart/form-data", info:""},
              {label: "text/css", type: "keyword", apply: "text/css", info:""},
              {label: "text/csv", type: "keyword", apply: "text/csv", info:""},
              {label: "text/html", type: "keyword", apply: "text/html", info:""},
              {label: "text/javascript (obsolete)", type: "keyword", apply: "text/javascript (obsolete)", info:""},
              {label: "text/plain", type: "keyword", apply: "text/plain", info:""},
              {label: "text/xml", type: "keyword", apply: "text/xml", info:""},
              {label: "video/mpeg", type: "keyword", apply: "video/mpeg", info:""},
              {label: "video/mp4", type: "keyword", apply: "video/mp4", info:""},
              {label: "video/quicktime", type: "keyword", apply: "video/quicktime", info:""},
              {label: "video/x-ms-wmv", type: "keyword", apply: "video/x-ms-wmv", info:""},
              {label: "video/x-msvideo", type: "keyword", apply: "video/x-msvideo", info:""},
              {label: "video/x-flv", type: "keyword", apply: "video/x-flv", info:""},
              {label: "video/webm", type: "keyword", apply: "video/webm", info:""},
              {label: "application/vnd.android.package-archive", type: "keyword", apply: "application/vnd.android.package-archive", info:""},
              {label: "application/vnd.oasis.opendocument.text", type: "keyword", apply: "application/vnd.oasis.opendocument.text", info:""},
              {label: "application/vnd.oasis.opendocument.spreadsheet", type: "keyword", apply: "application/vnd.oasis.opendocument.spreadsheet", info:""},
              {label: "application/vnd.oasis.opendocument.presentation", type: "keyword", apply: "application/vnd.oasis.opendocument.presentation", info:""},
              {label: "application/vnd.oasis.opendocument.graphics", type: "keyword", apply: "application/vnd.oasis.opendocument.graphics", info:""},
              {label: "application/vnd.ms-excel", type: "keyword", apply: "application/vnd.ms-excel", info:""},
              {label: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", type: "keyword", apply: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", info:""},
              {label: "application/vnd.ms-powerpoint", type: "keyword", apply: "application/vnd.ms-powerpoint", info:""},
              {label: "application/vnd.openxmlformats-officedocument.presentationml.presentation", type: "keyword", apply: "application/vnd.openxmlformats-officedocument.presentationml.presentation", info:""},
              {label: "application/msword", type: "keyword", apply: "application/msword", info:""},
              {label: "application/vnd.openxmlformats-officedocument.wordprocessingml.document", type: "keyword", apply: "application/vnd.openxmlformats-officedocument.wordprocessingml.document", info:""},
              {label: "application/vnd.mozilla.xul+xml", type: "keyword", apply: "application/vnd.mozilla.xul+xml", info:""}

            ]
          }
      }]
  })]
});

app.directive('tooltip', Tooltip);
app.mount('#app')