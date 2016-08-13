import React from 'react';
import { Route, IndexRoute } from 'react-router';
import MainContainer from '../containers/MainContainer';
import Home from '../components/Home';
import TaskTableContainer from '../containers/TaskTableContainer';
import TaskPreviewContainer from '../containers/TaskPreviewContainer';


const routes = (
  <Route path='/' component={MainContainer}>
    <IndexRoute component={Home} />
    <Route path='tasks' component={TaskTableContainer} />
    <Route path='task/:taskId' component={TaskPreviewContainer} />
  </Route>
);

export default routes;
