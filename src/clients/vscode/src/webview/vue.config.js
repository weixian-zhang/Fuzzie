const { defineConfig } = require('@vue/cli-service')
const path = require('path');
module.exports = defineConfig({
  disableHostCheck: true,
  filenameHashing: false,
  transpileDependencies: true,
  outputDir: path.resolve(__dirname, "../../vuejs-dist")
})
