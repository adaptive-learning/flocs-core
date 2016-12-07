import React from 'react';
import { connect } from 'react-redux';
import { CodeEditorContainer, SpaceGameContainer } from 'flocs-visual-components';
import { flocsActionCreators } from 'flocs-visual-components';


class TaskPreviewContainer extends React.Component {

  componentWillMount() {
    this.props.createTaskEnvironment(this.props.taskEnvironmentId);
    this.props.setTask(this.props.taskEnvironmentId, this.props.task);
  }

  render() {
    return (
      <div>
        <SpaceGameContainer taskEnvironmentId={this.props.taskEnvironmentId}/>
        <CodeEditorContainer taskEnvironmentId={this.props.taskEnvironmentId}/>
      </div>
    );
  }
}


function mapStateToProps(state, props) {
  // TODO: replace by object spread syntax
  const taskId = props.routeParams.taskId;
  return Object.assign({}, props, {
    taskEnvironmentId: "single",
    task: state.tasks[props.routeParams.taskId]
  });
};


export default connect(mapStateToProps, flocsActionCreators)(TaskPreviewContainer);
