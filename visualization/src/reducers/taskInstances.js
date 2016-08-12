import ActionTypes from '../actions/actionTypes';


function taskInstances(state={}, action) {
  switch (action.type) {
    case ActionTypes.TASKS.OPEN:
      return openTask(state, action.payload.taskId, action.payload.taskInstanceId);
    default:
      return state;
  }
}


function openTask(taskInstances, taskId) {
  // TODO:  check if a task has  already opened task instance...
  //if (taskId in taskInstances) {
  //  return taskInstances;
  //}
  const newTaskInstance = {
    id: 'tmp' + taskInstancesCounter++;
  };
  return Object.assign({}, state, {
          visibilityFilter: action.filter
        })

}

export default taskInstances;


/*const emptyTask = {
  name: '',
  setting: {
    fields: {
      '1-1': {background: 'black', objects: []},
      '1-2': {background: 'black', objects: []},
      '1-3': {background: 'black', objects: []},
      '2-1': {background: 'blue', objects: []},
      '2-2': {background: 'blue', objects: []},
      '2-3': {background: 'blue', objects: []},
    },
    start: 3,
  },
};

const task = (state = emptyTask, action) => {
  switch (action.type) {
    case 'TASK.SET':
      return action.task;
    default:
      return state;
  }
};

function todoApp(state = initialState, action) {
  switch (action.type) {
    case SET_VISIBILITY_FILTER:
      return Object.assign({}, state, {
        visibilityFilter: action.filter
      })
    default:
      return state
  }
}


export default task;*/
