import React from 'react';
import { Router, Route, Link, IndexRoute, hashHistory } from 'react-router'
import Main from '../components/Main'
import Home from '../components/Home'
import SpaceWorldContainer from '../containers/SpaceWorldContainer'

var routes = (
  <Router history={hashHistory}>
    <Route path='/' component={Main}>
      <IndexRoute component={Home} />
      <Route path='space-world' component={SpaceWorldContainer} />
    </Route>
  </Router>
);

export default routes;
