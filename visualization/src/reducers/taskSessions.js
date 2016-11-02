import ActionTypes from '../actions/actionTypes';


function reduceTaskSessions(state={}, action) {
  switch (action.type) {
    case ActionTypes.TASK_SESSION.CREATE:
      const { taskId, taskSessionId } = action.payload;
      return openTask(state, taskSessionId, taskId);
    case ActionTypes.TASK_SESSION.EXECUTE_COMMAND:
      return executeCommand(state, action.payload.taskSessionId, action.payload.command);
    default:
      return state;
  }
}


function openTask(taskSessions, taskSessionId, taskId) {
  const newTaskSession = {
    id: taskSessionId,
    taskId: taskId,
    code: {},
    commands: []
  };

  // TODO: rewrite using object spread syntax (babel plugin) or immutable.js
  return Object.assign({}, taskSessions, {
    [taskSessionId]: newTaskSession
  });
}


function executeCommand(taskSessions, taskSessionId, commandName) {
  const taskSession = taskSessions[taskSessionId];
  const updatedTaskSession = Object.assign({}, taskSession, {
    commands: [...taskSession.commands, commandName]
  });
  // TODO: rewrite using object spread syntax (babel plugin) or immutable.js
  return Object.assign({}, taskSessions, {
    [taskSessionId]: updatedTaskSession
  });
}


export default reduceTaskSessions;
