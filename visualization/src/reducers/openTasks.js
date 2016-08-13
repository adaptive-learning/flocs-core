import ActionTypes from '../actions/actionTypes';


function reduceOpenTasks(state={}, action) {
  switch (action.type) {
    case ActionTypes.TASK_INSTANCE.CREATE:
      const { taskId, taskInstanceId } = action.payload;
      return openTask(state, taskId, taskInstanceId);
    default:
      return state;
  }
}


function openTask(tasks, taskId, taskInstanceId) {
  // TODO: rewrite using object spread syntax (babel plugin) or immutable.js
  return Object.assign({}, tasks, {
    [taskId]: taskInstanceId,
  });
}


export default reduceOpenTasks;
