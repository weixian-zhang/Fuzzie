import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import "@mdi/font/css/materialdesignicons.css";
import { loadFonts } from './plugins/webfontloader'

import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';
// import 'material-design-icons-iconfont/dist/material-design-icons.css'

loadFonts()

createApp(App)
  .use(vuetify)
  .mount('#app')
