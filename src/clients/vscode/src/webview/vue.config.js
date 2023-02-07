const { defineConfig } = require('@vue/cli-service')
const { VuetifyPlugin } = require('webpack-plugin-vuetify')

const path = require('path');
module.exports = defineConfig({
  filenameHashing: false,
  transpileDependencies: true,
  //adding extract css true solves this issue
  css:{
    extract:true  
  },
  outputDir: path.resolve(__dirname, "../../dist/webview"),
  publicPath: './',
  pluginOptions: {
    vuetify: new VuetifyPlugin()
  },
  configureWebpack: {
    devtool: "source-map",
    module: {
      rules: [
        {
          test: /\.js$/,
          enforce: 'pre',
          use: ['source-map-loader'],
        },
      ]
    }
  }
})



