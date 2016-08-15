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
//import { fetchTasksIfNeeded } from './actions/tasks';
//store.dispatch(fetchTasksIfNeeded()).then(() =>
//  console.log('state', store.getState())
//);
//store.dispatch(createTaskInstanceIfNotExist(1));
//store.dispatch(createTaskInstanceIfNotExist(1));
//console.log(store.getState());
