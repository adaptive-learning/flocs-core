import axios from 'axios'


const FAKE_TASKS = {
  1: {
    id: 1,
    ref: 'zig-zag',
    setting: {
      fields: [[['b', []], ['b', []], ['b', []], ['b', []], ['b', []]], [['k', ['R']], ['k', []], ['k', ['R']], ['k', []], ['k', ['R']]], [['k', []], ['k', ['R']], ['k', []], ['k', ['R']], ['k', []]], [['k', ['R']], ['k', []], ['k', ['R']], ['k', []], ['k', ['R']]], [['k', []], ['k', ['R']], ['k', []], ['k', ['R']], ['k', []]], [['k', ['R']], ['k', []], ['k', ['R']], ['k', []], ['k', ['R']]], [['k', []], ['k', ['R']], ['k', []], ['k', ['R']], ['k', []]], [['k', ['R']], ['k', []], ['k', ['R']], ['k', []], ['k', ['R']]], [['k', []], ['k', []], ['k', ['S']], ['k', []], ['k', []]]],
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
