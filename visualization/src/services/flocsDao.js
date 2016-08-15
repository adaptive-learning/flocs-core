import axios from 'axios'


const FAKE_TASKS = {
  1: {
    id: 1,
    ref: 'zig-zag',
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
    solution: 'TBA',
  },
  2: {
    id: 2,
    ref: 'asteroid stripes',
    setting: 'TBA',
    solution: 'TBA',
  }
};


var flocsDao = {
  fetchTasks: function() {
    /*axios.get('/task/' + key)
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    */
    return new Promise(resolve => resolve(FAKE_TASKS));
  }
};

export default flocsDao;
