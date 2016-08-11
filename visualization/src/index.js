import React from 'react';
import ReactDOM from 'react-dom';
import { createStore } from 'redux';
import { Provider } from 'react-redux';
import routes from './config/routes';
import reducers from './reducers'

import Main from './components/Main'  // TODO: user router instead and remove this import
import Home from './components/Home'  // TODO: user router instead and remove this import


// quick test
import { run } from './actions/task'
console.log(run());

let store = createStore(reducers);
ReactDOM.render(
  <Provider store={store}>
    <Main><Home/></Main>
  </Provider>,
  //routes,
  document.getElementById('flocsApp')
);
