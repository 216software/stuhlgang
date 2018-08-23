const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: './src/js/index.js',

  devtool: 'source-map',

  output: {
    filename: '[name].[hash].js',
    path: path.resolve(__dirname, 'www'),
  },

  module: {
    rules: [
      // babel loader
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
            plugins: ['transform-class-properties'],
          },
        },
      },

      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          { loader: 'css-loader' },
          {
            loader: 'postcss-loader',
            options: {
              // eslint-disable-next-line
              plugins: function () {
                return [
                  // eslint-disable-next-line
                  require('precss'),
                  // eslint-disable-next-line
                  require('autoprefixer'),
                ];
              },
            },
          },
          { loader: 'sass-loader' },
        ],
      },

      /*
      // sass loader
      {
        test: /\.(scss)$/,
        use: [
          { loader: 'style-loader' },
          { loader: 'css-loader' },
          {
            loader: 'postcss-loader',
            options: {
              // eslint-disable-next-line
              plugins: function () {
                return [
                  // eslint-disable-next-line
                  require('precss'),
                  // eslint-disable-next-line
                  require('autoprefixer'),
                ];
              },
            },
          },
          { loader: 'sass-loader' },
        ],
      },
      */

      // html loader
      {
        test: /\.html$/,
        use: {
          loader: 'html-loader',
          options: { minimize: true },
        },
      },
    ],
  },

  plugins: [
    new webpack.NamedModulesPlugin(),

    // ensure that globally accessed variables in 3rd party libraries are
    // defined (knockout, pager, bootstrap)
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      ko: 'knockout',
    }),

    // clean out the www folder between builds to prevent old files from piling
    // up
    new CleanWebpackPlugin([
      'www/',
    ]),

    new MiniCssExtractPlugin({
      filename: '[name].[hash].css',
      chunkFilename: '[id].[hash].css',
    }),

    // copy all the template files so that the app can access them.
    new CopyWebpackPlugin([
      {
        from: './src/templates/**/*',
        to: 'templates',
        flatten: true,
      },
    ]),

    // use a template to define the index file
    new HtmlWebpackPlugin({
      filename: 'index.html',
      template: 'src/index.html',
    }),
  ],
};
