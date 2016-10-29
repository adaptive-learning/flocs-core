import ActionTypes from '../actions/actionTypes';
import TASKS_LIST from '../../exported_data/tasks';

// create a map of tasks from a list of tasks
let TASKS = {};
TASKS_LIST.forEach(task => { TASKS[task.taskId] = task; });


function reduceTasks(state=TASKS, action) {
  return state;
}


export default reduceTasks;
