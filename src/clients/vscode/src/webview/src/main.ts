import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import "@mdi/font/css/materialdesignicons.css";
import { loadFonts } from './plugins/webfontloader'

import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/saga-blue/theme.css'      //theme
import 'primevue/resources/primevue.min.css'                //core css
import 'primeicons/primeicons.css'                         //icons


import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';

loadFonts()

const app = createApp(App);
app.use(vuetify)
app.use(PrimeVue)
app.mount('#app')