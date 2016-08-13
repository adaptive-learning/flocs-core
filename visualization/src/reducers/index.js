import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux'
import tasks from './tasks'
import taskInstances from './taskInstances'
import openTasks from './openTasks'

const reducers = combineReducers({
  tasks, taskInstances,
  openTasks,
  routing: routerReducer
});


export default reducers;
