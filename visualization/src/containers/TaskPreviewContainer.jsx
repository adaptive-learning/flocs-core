import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import { TaskEnvironmentContainer,
         flocsActionCreators } from 'flocs-visual-components';


class TaskPreviewWrapper extends React.Component {

  componentWillMount() {
    this.props.setTask(this.props.taskEnvironmentId, this.props.task);
  }

  render() {
    return (
      <TaskEnvironmentContainer taskEnvironmentId={this.props.taskEnvironmentId} />
    );
  }
}

TaskPreviewWrapper.propTypes = {
  taskEnvironmentId: PropTypes.string.isRequired,
  task: PropTypes.object.isRequired,
  createTaskEnvironment: PropTypes.func.isRequired,
  setTask: PropTypes.func.isRequired,
};


function mapStateToProps(state, props) {
  // TODO: replace by object spread syntax
  return Object.assign({}, props, {
    taskEnvironmentId: 'single',
    task: state.tasks[props.routeParams.taskId],
  });
}


export default connect(mapStateToProps, flocsActionCreators)(TaskPreviewWrapper);
