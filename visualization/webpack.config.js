var CopyWebpackPlugin = require('copy-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var webpack = require("webpack");

module.exports = {
  devtool: "source-map",
  entry: [
    'webpack-dev-server/client?http://0.0.0.0:8080',
    'webpack/hot/only-dev-server', // "only" prevents reload on syntax errors
    './src/index.jsx',
  ],
  devServer: {
    inline: true,
    historyApiFallback: true,
    // on refresh, always look for index.html (on any path)
  },
  output: {
    path: __dirname + '/dist',
    publicPath: '/',
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
      },
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader',
      },
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
