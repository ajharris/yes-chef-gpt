const path = require('path');

module.exports = {
    mode: 'development',  // Change to 'production' for production builds
    entry: './src/index.js',
    output: {
        path: path.resolve(__dirname, 'dist'),  // Output folder
        filename: 'bundle.js',
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                },
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],  // Load CSS files
            },
        ],
    },
    devServer: {
        static: './dist',
    },
};
