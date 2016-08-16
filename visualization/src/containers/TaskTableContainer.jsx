import React from 'react';
import { connect } from 'react-redux';
import * as tasksActions from '../actions/tasks';
import TaskTable from '../components/TaskTable';
import { fetchTasksIfNeeded } from '../actions/tasks';


class TaskTableContainer extends React.Component {
  render() {
    return (
      <TaskTable tasks={this.props.tasks}/>
    );
  }

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch(fetchTasksIfNeeded());
  }
}


function mapStateToProps(state) {
  return {
    tasks: state.tasks
  };
};


const ConnectedTaskTableContainer = connect(mapStateToProps)(TaskTableContainer);
export default ConnectedTaskTableContainer;
