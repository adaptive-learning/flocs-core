import ActionTypes from '../actions/actionTypes';

const FAKE_TASKS = {
  1: {
    id: 1,
    ref: 'zig-zag',
    setting: 'TBA',
    solution: 'TBA',
  }
};

function tasks(state={}, action) {
  switch (action.type) {
    case ActionTypes.TASKS.FETCH:
      return FAKE_TASKS;
    case ActionTypes.TASKS.OPEN:
      return tasks;
    default:
      return state;
  }
}


export default tasks;

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
