import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import * as tasksActions from '../actions/tasks';
import TaskPreview from '../components/TaskPreview';
import gameState from '../extractors/gameState';


class TaskPreviewContainer extends React.Component {
  componentDidMount() {
    const { createTaskSessionIfNotExist, taskId } = this.props;
    createTaskSessionIfNotExist(taskId);
  }

  render() {
    return (
      <TaskPreview
        fields={this.props.fields}
        handleCommand={this.handleCommand.bind(this)}
        code={this.props.code}
        handleCodeChange={this.handleCodeChange.bind(this)}
      />
    );
  }

  handleCommand(commandName) {
    switch (commandName) {
      case 'left':
      case 'right':
      case 'ahead':
      case 'ahead+shot':
        this.props.executeCommand(this.props.taskSessionId, commandName);
        break;
      case 'run':
        this.props.runProgram(this.props.taskSessionId);
        break;
      case 'reset':
        this.props.resetWorld(this.props.taskSessionId);
        break;
      default:
        throw 'Undefined control command ' + commandName;
    }
  }

  handleCodeChange(code) {
    // TODO/QUESTION: find if changing store on every code change is a good
    // idea
    this.props.changeCode(this.props.taskSessionId, code);
  }
}


const mapStateToProps = (state, props) => {
  const { taskId } = props.params;
  const task = state.tasks[taskId];
  const taskSessionId = extractTaskSessionId(state, taskId);
  const fields = (taskSessionId === null) ? task.setting.fields : gameState(state, taskSessionId).fields;
  const code = (taskSessionId === null) ? '' : state.taskSessions[taskSessionId].code;
  return { taskId, task, taskSessionId, fields, code };
};


function extractTaskSessionId(state, taskId) {
  if (!(taskId in state.openTasks)) {
    return null;
  }
  const taskSessionId = state.openTasks[taskId];
  return taskSessionId;
}


const mapDispatchToProps = (dispatch) => {
  return bindActionCreators(tasksActions, dispatch);
};


const ConnectedTaskPreviewContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(TaskPreviewContainer);
export default ConnectedTaskPreviewContainer;
