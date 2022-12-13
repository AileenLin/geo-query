const { defineConfig } = require('@vue/cli-service')
module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? '/geo-query/'
    : '/'
  // devServer: {
  //   proxy: {
  //     '/V1': {
  //       target: 'https://www.wikidata.org/w/api.php?',
  //       changeOrigin: true,
  //       pathRewrite: {
  //         '^/V1': ''
  //       }
  //     },
  //     '/V2': {
  //       target: 'https://loclhost:4437',
  //       changeOrigin: true,
  //       pathRewrite: {
  //         '^/V2': ''
  //       }
  //     }
  //   }
  // }
}
