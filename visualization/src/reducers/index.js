import { combineReducers } from 'redux';
import tasks from './tasks'
import taskInstances from './taskInstances'


const reducers = combineReducers({
  tasks, taskInstances
});


export default reducers;
