var CopyWebpackPlugin = require('copy-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var webpack = require("webpack");

module.exports = {
  devtool: "source-map",
  entry: [
    'webpack-dev-server/client?http://0.0.0.0:8080', // WebpackDevServer host and port
    'webpack/hot/only-dev-server', // "only" prevents reload on syntax errors
    './src/index.js',
  ],
  output: {
    path: __dirname + '/dist',
    filename: 'bundle.js'
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  },
  module: {
    loaders: [
      { test: /.jsx?$/
      , loader: 'babel'
      , exclude: /node_modules/
      , query: { presets: ['es2015', 'react', 'react-hmre'] }
      }
    ]
  },
  plugins: [
    new CopyWebpackPlugin([
      { from: 'node_modules/flocs-visual-components/lib/static/images'
      , to: 'static/images'
      },
    ]),
    new HtmlWebpackPlugin({
      template: __dirname + '/src/index.html',
      filename: 'index.html',
      inject: 'body'
    }),
  ]
};
