import { connect } from 'react-redux';
import { TasksTable } from 'flocs-visual-components';


function mapStateToProps(state) {
  return {
    tasks: Object.values(state.tasks),
  };
}


const TasksTableContainer = connect(mapStateToProps)(TasksTable);
export default TasksTableContainer;
