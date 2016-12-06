import ActionTypes from '../actions/actionTypes';


function reduceOpenTasks(state={}, action) {
  switch (action.type) {
    case ActionTypes.TASK_SESSION.CREATE:
      const { taskId, taskSessionId } = action.payload;
      return openTask(state, taskId, taskSessionId);
    default:
      return state;
  }
}


function openTask(tasks, taskId, taskSessionId) {
  // TODO: rewrite using object spread syntax (babel plugin) or immutable.js
  return Object.assign({}, tasks, {
    [taskId]: taskSessionId,
  });
}


export default reduceOpenTasks;
