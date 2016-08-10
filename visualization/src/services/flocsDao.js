import axios from 'axios'

var flocsDao = {
  gettingTaskByKey: function(key) {
    /*axios.get('/task/' + key)
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    */
    const FAKE_TASK = {
      name: 'zig-zag',
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
    return new Promise(resolve => resolve(FAKE_TASK));
  }
};

export default flocsDao;
