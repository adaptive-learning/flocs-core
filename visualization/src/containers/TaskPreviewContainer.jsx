import { connect } from 'react-redux';
import * as tasksActions from '../actions/tasks';
import TaskPreview from '../components/TaskPreview';


const mapStateToProps = (state) => {
  return {
    task: state.task
  };
};


const mapDispatchToProps = (dispatch) => {
  return {};  // TBA
};

const TaskPreviewContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(TaskPreview);


export default TaskPreviewContainer;
