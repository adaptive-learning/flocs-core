import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRoute, browserHistory } from 'react-router';
import { createStore, combineReducers, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import createLogger from 'redux-logger';
import { Provider } from 'react-redux';
import { flocsComponentsReducer } from 'flocs-visual-components';
import tasksReducer from './reducers/tasks';
import MainContainer from './containers/MainContainer';
import TasksTableContainer from './containers/TasksTableContainer';
import TaskPreviewContainer from './containers/TaskPreviewContainer';


function createTaskAppComponent() {
  const appComponent = (
    <Provider store={createAppStore()}>
      <Router history={browserHistory}>
        {createRoutes()}
      </Router>
    </Provider>
  );
  return appComponent;
}


function createAppStore() {
  const rootReducer = combineReducers({
    tasks: tasksReducer,
    flocsComponents: flocsComponentsReducer,
  });
  const logger = createLogger();
  const middleware = applyMiddleware(thunk, logger);
  const store = createStore(rootReducer, middleware);
  return store;
}


function createRoutes() {
  const routes = (
    <Route path="/" component={MainContainer}>
      <IndexRoute component={TasksTableContainer} />
      <Route path="/task/:taskId" component={TaskPreviewContainer} />
    </Route>
  );
  return routes;
}


const mountElement = document.getElementById('flocsTasksApp');
const appComponent = createTaskAppComponent();
ReactDOM.render(appComponent, mountElement);
