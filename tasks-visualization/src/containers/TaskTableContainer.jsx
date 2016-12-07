import React from 'react';
import { connect } from 'react-redux';
import TaskTable from '../components/TaskTable';


class TaskTableContainer extends React.Component {
  render() {
    return (
      <TaskTable tasks={this.props.tasks}/>
    );
  }
}


function mapStateToProps(state) {
  return {
    tasks: state.tasks
  };
};


const ConnectedTaskTableContainer = connect(mapStateToProps)(TaskTableContainer);
export default ConnectedTaskTableContainer;
