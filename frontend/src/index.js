import { AppRegistry } from 'react-native';
import App from './App'; // Make sure this is pointing to App.js
import { createRoot } from 'react-dom/client';
import { Platform } from 'react-native';
import 'bootstrap/dist/css/bootstrap.min.css';


if (Platform.OS === 'web') {
  const rootElement = document.getElementById('root');
  const root = createRoot(rootElement);
  root.render(<App />);
} else {
  AppRegistry.registerComponent('main', () => App);
  AppRegistry.runApplication('main', {
    initialProps: {},
    rootTag: document.getElementById('root'),
  });
}
