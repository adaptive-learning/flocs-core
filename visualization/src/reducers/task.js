const emptyTask = {
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

export default task;
