import ActionTypes from '../actions/actionTypes';


function reduceTaskInstances(state={}, action) {
  switch (action.type) {
    case ActionTypes.TASK_INSTANCE.CREATE:
      const { taskId, taskInstanceId } = action.payload;
      return openTask(state, taskInstanceId, taskId);
    default:
      return state;
  }
}


function openTask(taskInstances, taskInstanceId, taskId) {
  const newTaskInstance = {
    id: taskInstanceId,
    taskId: taskId,
    code: {},
    commands: []
  };

  // TODO: rewrite using object spread syntax (babel plugin) or immutable.js
  return Object.assign({}, taskInstances, {
    [taskInstanceId]: newTaskInstance
  });
}


export default reduceTaskInstances;


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
