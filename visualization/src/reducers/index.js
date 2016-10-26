import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux'
import tasks from './tasks'
import taskSessions from './taskSessions'
import openTasks from './openTasks'

const reducers = combineReducers({
  tasks, taskSessions,
  openTasks,
  routing: routerReducer
});


export default reducers;
