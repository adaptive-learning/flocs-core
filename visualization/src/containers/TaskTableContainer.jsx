import { connect } from 'react-redux';
import * as tasksActions from '../actions/tasks';
import TaskTable from '../components/TaskTable';


const mapStateToProps = (state) => {
  return {
    task: state.task
  };
};


const mapDispatchToProps = (dispatch) => {
  return {};  // TBA
};

const TaskTableContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(TaskTable);

export default TaskTableContainer;
