const { defineConfig } = require('@vue/cli-service')
const path = require('path');
module.exports = defineConfig({
  filenameHashing: false,
  transpileDependencies: true,
  css: undefined,
  outputDir: path.resolve(__dirname, "../../dist/webview"),

  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  }
})
