import ActionTypes from '../actions/actionTypes';


function reduceTaskSessions(state={}, action) {
  switch (action.type) {
    case ActionTypes.TASK_SESSION.CREATE:
      const { taskId, taskSessionId } = action.payload;
      return openTask(state, taskSessionId, taskId);
    case ActionTypes.TASK_SESSION.EXECUTE_COMMAND:
      return executeCommand(state, action.payload.taskSessionId, action.payload.commandName);
    case ActionTypes.TASK_SESSION.RESET:
      return resetWorld(state, action.payload.taskSessionId);
    default:
      return state;
  }
}


function openTask(taskSessions, taskSessionId, taskId) {
  const newTaskSession = {
    id: taskSessionId,
    taskId: taskId,
    //program: [['repeat', 3, [['move', 'right'], ['move', 'left']]]],  // fake some program for test purposes {}, TODO: UPDATE_program action
    program: [["while", ["position", "<", "5"], [["move", "right"]]],["while", ["position", ">", "1"], [["move", "left"]]]],
    commands: []
  };

  // TODO: rewrite using object spread syntax (babel plugin) or immutable.js
  return Object.assign({}, taskSessions, {
    [taskSessionId]: newTaskSession
  });
}


function executeCommand(taskSessions, taskSessionId, commandName) {
  const taskSession = taskSessions[taskSessionId];
  const updatedCommands = [...taskSession.commands, commandName];
  const updatedTaskSession = Object.assign({}, taskSession, {
    commands: updatedCommands
  });
  // TODO: rewrite using object spread syntax (babel plugin) or immutable.js
  return Object.assign({}, taskSessions, {
    [taskSessionId]: updatedTaskSession
  });
}


function resetWorld(taskSessions, taskSessionId) {
  const taskSession = taskSessions[taskSessionId];
  const updatedTaskSession = Object.assign({}, taskSession, {
    commands: []
  });
  return Object.assign({}, taskSessions, {
    [taskSessionId]: updatedTaskSession
  });
}


export default reduceTaskSessions;
