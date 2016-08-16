import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import * as tasksActions from '../actions/tasks';
import TaskPreview from '../components/TaskPreview';


class TaskPreviewContainer extends React.Component {
  componentDidMount() {
    // TODO: should also fetch task(s) if needed? (to enable direct access)
    const { createTaskInstanceIfNotExist, taskId } = this.props;
    createTaskInstanceIfNotExist(taskId);
  }

  render() {
    return (
      <TaskPreview task={this.props.task} blocks={this.props.blocks}/>
    );
  }
}


const mapStateToProps = (state, props) => {
  const { taskId } = props.params;
  const task = state.tasks[taskId];
  //const taskInstanceId = state.openTasks[taskId];
  //const taskInstance = state.taskInstances[taskInstanceId];
  //console.log('in mapStateToProps', task, taskInstance);
  // TODO: use task and task instance (if available) to build current state
  const blocks = getBlocksList(task.setting);
  // TODO: props contains non-normalized (duplicate) data, is it ok? (probably
  // yes, as it's just derived data, not the source of truth)
  return { taskId, task, blocks };
};


const getBlocksList = (setting) => {
  if (!setting) {
    return [];
  }
  var blocks = []
  for (var position in setting.fields) {
    blocks.push({position: position, name: setting.fields[position].background});
    // TBA: push all objects on this position as well
  }
  var heroPosition = '0-' + setting.start;
  blocks.push({position: heroPosition, name: 'space-rocket'});
  // TODO: pass and apply commands ?
  return blocks;
}



const mapDispatchToProps = (dispatch) => {
  return bindActionCreators(tasksActions, dispatch);
};


const ConnectedTaskPreviewContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(TaskPreviewContainer);
export default ConnectedTaskPreviewContainer;