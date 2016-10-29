import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import * as tasksActions from '../actions/tasks';
import TaskPreview from '../components/TaskPreview';


class TaskPreviewContainer extends React.Component {
  componentDidMount() {
    const { createTaskSessionIfNotExist, taskId } = this.props;
    createTaskSessionIfNotExist(taskId);
  }

  render() {
    return (
      <TaskPreview fields={this.props.fields} handleCommand={this.handleCommand.bind(this)} />
    );
  }

  handleCommand(command) {
    this.props.executeCommand(this.props.taskSessionId, command);
  }
}


const mapStateToProps = (state, props) => {
  const { taskId } = props.params;
  const task = state.tasks[taskId];
  const taskSessionId = extractTaskSessionId(state, taskId);
  const fields = (taskSessionId === null) ? task.setting.fields : computeCurrentFields(state, taskSessionId);
  return { taskId, task, taskSessionId, fields };
};


function extractTaskSessionId(state, taskId) {
  if (!(taskId in state.openTasks)) {
    return null;
  }
  const taskSessionId = state.openTasks[taskId];
  return taskSessionId;
}


function computeCurrentFields(state, taskSessionId) {
  const taskSession = state.taskSessions[taskSessionId];
  const task = state.tasks[taskSession.taskId];
  const fields = runCommands(task.setting.fields, taskSession.commands);
  return fields;
}


function runCommands(fields, commands) {
  return commands.reduce(runCommand, fields);
}


function runCommand(fields, command) {
  const oldSpaceshipPosition = findSpaceshipPosition(fields);
  const horizontalShift = {'left': -1, 'ahead': 0, 'right': 1}[command.direction];
  const newSpaceshipPosition = [oldSpaceshipPosition[0] - 1, oldSpaceshipPosition[1] + horizontalShift];
  const newFields = fields.map(function (row, i) {
    return row.map(function (field, j) {
      let [background, objects] = field;
      if (i == oldSpaceshipPosition[0] && j == oldSpaceshipPosition[1]) {
        objects = [];
      }
      if (i == newSpaceshipPosition[0] && j == newSpaceshipPosition[1]) {
        objects = [...objects, 'S'];
      }
      return [background, objects];
    });
  });
  return newFields;
}


function findSpaceshipPosition(fields) {
  for (let i=0; i<fields.length; i++)  {
    for (let j=0; j<fields[i].length; j++)  {
      const objects = fields[i][j][1];
      if (objects.indexOf('S') >= 0) {
        return [i, j];
      }
    }
  }
}


const mapDispatchToProps = (dispatch) => {
  return bindActionCreators(tasksActions, dispatch);
};


const ConnectedTaskPreviewContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(TaskPreviewContainer);
export default ConnectedTaskPreviewContainer;
