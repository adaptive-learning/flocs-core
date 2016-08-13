import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, applyMiddleware, compose } from 'redux';
import { Provider } from 'react-redux';
import { Router, Route, IndexRoute, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux'
import thunk from 'redux-thunk';
import createLogger from 'redux-logger';
import routes from './config/routes';
import reducers from './reducers';

import Main from './components/Main';  // TODO: user router instead and remove this import
import Home from './components/Home';  // TODO: user router instead and remove this import


const logger = createLogger();
const store = createStore(reducers, compose(
  applyMiddleware(thunk, logger),
  window.devToolsExtension ? window.devToolsExtension() : f => f
));


const history = syncHistoryWithStore(browserHistory, store);
const app = (
  <Provider store={store}>
    <Router history={history}>
      {routes}
    </Router>
  </Provider>
);
const mountElement = document.getElementById('flocsApp')

ReactDOM.render(app, mountElement);


// quick test
import { fetch, createTaskInstanceIfNotExist } from './actions/tasks';
store.dispatch(fetch());
store.dispatch(createTaskInstanceIfNotExist(1));
store.dispatch(createTaskInstanceIfNotExist(1));
console.log(store.getState());
//let s1 = reducers({}, fetch());
//console.log(s1);
//let s2 = reducers(s1, open(1));
//console.log(s2);

