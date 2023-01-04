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
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';

import Logger from './Logger';

import { basicSetup } from 'codemirror'
import VueCodemirror from 'vue-codemirror'
import {json} from "@codemirror/lang-json"
import {CompletionContext, autocompletion} from "@codemirror/autocomplete"

const logger = new Logger();

loadFonts()

const app = createApp(App);
app.provide("$logger", logger); // gloval singleton instance of logger
app.use(vuetify)
app.use(PrimeVue)
app.use(ToastService);
//https://github.com/surmon-china/vue-codemirror/issues/171
app.use(VueCodemirror, {
  // optional default global options
  autofocus: true,
  disabled: false,
  indentWithTab: true,
  tabSize: 2,
  //placeholder: 'Code goes here...',
  extensions: [json(), basicSetup, autocompletion({
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
            {label: "pdf", type: "keyword", apply: "{{ pdf }}", info:"PDF mix with other file types encode with 'latin1'"},
            {label: "file", type: "keyword", apply: "{{ file }}", info:"danielmiessler's seclist payload encode with 'latin1'"},
            {label: "datetime", type: "keyword", apply: "{{ datetime  }}", info:"date & time"},
            {label: "date", type: "keyword", apply: "{{ date  }}", info:"date only"},
            {label: "time", type: "keyword", apply: "{{ time  }}", info:"time only"},
            {label: "username", type: "keyword", apply: "{{ username  }}", info:"usernames from danielmiessler's seclist"},
            {label: "password", type: "keyword", apply: "{{ password  }}", info:"password from danielmiessler's seclist"},
            {label: "filename", type: "keyword", apply: "{{ filename  }}", info:""},
            {label: "string", type: "keyword", apply: "{{ string  }}", info:"minimaxir/big-list-of-naughty-strings"},
          ]
        }
    }]
  })]
});

app.directive('tooltip', Tooltip);
app.mount('#app')