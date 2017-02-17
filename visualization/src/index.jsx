import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRoute, browserHistory } from 'react-router';
import { FlocsProvider } from 'flocs-visual-components';
import tasksReducer from './reducers/tasks';
import MainContainer from './containers/MainContainer';
import TasksTableContainer from './containers/TasksTableContainer';
import TaskPreviewContainer from './containers/TaskPreviewContainer';

const reducers = {
  tasks: tasksReducer,
};

const appComponent = (
  <FlocsProvider reducers={reducers}>
    <Router history={browserHistory}>
      <Route path="/" component={MainContainer}>
        <IndexRoute component={TasksTableContainer} />
        <Route path="/task/:taskId" component={TaskPreviewContainer} />
      </Route>
    </Router>
  </FlocsProvider>
);

const mountElement = document.getElementById('flocsVisualizationApp');
ReactDOM.render(appComponent, mountElement);
