const { defineConfig } = require('@vue/cli-service')
const path = require('path');
module.exports = defineConfig({
  filenameHashing: false,
  transpileDependencies: true,
  css: undefined,
  outputDir: path.resolve(__dirname, "../../dist/webview")
  // chainWebpack: (config) => {
  //   config.plugin('copy').tap((entries) => {
  //     entries[0].patterns.push({
  //       from: path.resolve(__dirname, '/src/assets'),
  //       to: path.resolve(__dirname, '../../dist/webview/assets'),
  //       toType: 'dir',
  //       noErrorOnMissing: true,
  //       globOptions: { ignore: ['.DS_Store'] },
  //     })

  //     return entries
  //   })
  // }
})
