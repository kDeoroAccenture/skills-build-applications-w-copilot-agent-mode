import React from 'react';
import { createRoot } from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import App from './App';

const container = document.getElementById('root');
const root = createRoot(container);
console.log('REACT_APP_CODESPACE_NAME=', process.env.REACT_APP_CODESPACE_NAME);

root.render(
	<React.StrictMode>
		<App />
	</React.StrictMode>
);
