import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';  // Ensure the path is correct

ReactDOM.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
    document.getElementById('root')  // Must match <div id="root"></div> in index.html
);
