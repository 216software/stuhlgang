const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HardSourcePlugin = require('hard-source-webpack-plugin');

// eslint-disable-next-line
module.exports = (env) => {
  return {
    entry: ['babel-polyfill', './src/js/index.js'],

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

        // load fonts
        {
          test: /.(ttf|otf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/,
          exclude: /images/,
          use: [{
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'fonts/',
              publicPath: '../fonts/',
            },
          }],
        },

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

      // Try to speed up build times
      new HardSourcePlugin(),

      // ensure that globally accessed variables in 3rd party libraries are
      // defined (knockout, pager, bootstrap)
      new webpack.ProvidePlugin({
        $: 'jquery',
        jQuery: 'jquery',
        'window.jQuery': 'jquery',
        Popper: ['popper.js', 'default'],
        ko: 'knockout',
      }),

      // clean out the www folder between builds to prevent old files from piling
      // up
      new CleanWebpackPlugin([
        'www/',
      ]),

      new MiniCssExtractPlugin({
        filename: 'css/[name].[hash].css',
        chunkFilename: 'css/[id].[hash].css',
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

      new webpack.DefinePlugin({
        API_URL: env.NODE_ENV === 'production' ? JSON.stringify('production-url') : JSON.stringify('https://stuhlgang-dev.216software.com/api'),
      }),
    ],
  };
};
