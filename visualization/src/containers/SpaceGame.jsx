import { connect } from 'react-redux';
import * as tasksActions from '../actions/tasks';
import SpaceWorldWithControls from '../components/SpaceWorldWithControls';


/*
  componentDidMount() {
    // TODO: use store
    var key = 'zig-zag'
    flocsDao.gettingTaskByKey(key).then(function(task) {
      this.setState({
        fields: task.setting.fields,
        hero: {x: task.setting.start, y: 1}
      });
    }.bind(this));
  }
*/

const mapStateToProps = (state) => {
  return {
    task: state.task
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};  // TBA
};

const SpaceGame = connect(
  mapStateToProps,
  mapDispatchToProps
)(SpaceWorldWithControls);

export default SpaceGame;
