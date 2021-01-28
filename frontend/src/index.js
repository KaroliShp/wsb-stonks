import React from 'react';
import ReactDOM from 'react-dom';
import CssBaseline from '@material-ui/core/CssBaseline';
import { ThemeProvider } from '@material-ui/core/styles';
import App from './App';
import theme from './theme';
import * as Sentry from '@sentry/browser'
import ReactGA from 'react-ga'

/*
if (process.env.NODE_ENV === 'production') {
  Sentry.init({
    dsn: "https://d20d50d40ae544d9ab388546cc53b1ec@o378312.ingest.sentry.io/5201553"
  });
}
*/

ReactGA.initialize('UA-167581211-1');
ReactGA.pageview(window.location.pathname + window.location.search);

ReactDOM.render(
  <ThemeProvider theme={theme}>
    {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
    <CssBaseline />
    <App />
  </ThemeProvider>,
  document.querySelector('#root'),
);
