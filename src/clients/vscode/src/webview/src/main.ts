import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import "@mdi/font/css/materialdesignicons.css";
import { loadFonts } from './plugins/webfontloader'

import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/saga-blue/theme.css'      //theme
import 'primevue/resources/primevue.min.css'                //core css
import 'primeicons/primeicons.css'                         //icons


// <link href="https://unpkg.com/primevue@^3/resources/themes/saga-blue/theme.css" rel="stylesheet" />
// <link href="https://unpkg.com/primevue@^3/resources/primevue.min.css" rel="stylesheet" />
// <link href="https://unpkg.com/primeflex@^3/primeflex.min.css" rel="stylesheet" />
// <link href="https://unpkg.com/primeicons/primeicons.css" rel="stylesheet" />

import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';

loadFonts()

const app = createApp(App);
app.use(vuetify)
app.use(PrimeVue)
app.mount('#app')