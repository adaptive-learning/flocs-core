import ActionTypes from './actionTypes';
import flocsDao from '../services/flocsDao';


let nextTaskSessionId = 0;


export function fetchTaskIfNeeded(taskId) {
  const action = function(dispatch, getState) {
    if (shouldFetchTask(getState(), taskId)) {
      // TODO: fetch single task only
      return dispatch(fetchTasks())
    } else {
      return Promise.resolve()
    }
  };
  return action;
}


export function fetchTasksIfNeeded() {
  const action = function(dispatch, getState) {
    if (shouldFetchTasks(getState())) {
      return dispatch(fetchTasks())
    } else {
      return Promise.resolve()
    }
  };
  return action;
}


function shouldFetchTask(state, taskId) {
  return !(taskId in state.tasks);
}


function shouldFetchTasks(state) {
  // TODO: better way to find if the tasks were not fetched yet?
  return (Object.keys(state.tasks).length === 0);
}


function fetchTasks() {
  const action = function(dispatch) {
    dispatch(requestTasks());
    return flocsDao.fetchTasks().then(tasks => dispatch(receiveTasks(tasks)));
  };
  return action;
}


export function requestTasks() {
  return {
    type: ActionTypes.TASKS.REQUEST,
  };
};


export function receiveTasks(tasks) {
  return {
    type: ActionTypes.TASKS.RECEIVE,
    payload: { tasks },
  };
};



export function createTaskSessionIfNotExist(taskId) {
  // TODO: think and refactor (make it readable)
  return function(dispatch, getState) {
    // TODO: does this logic belong here?
    if (!(taskId in getState().openTasks)) {
      dispatch(createTaskSession(taskId));
    }
  };
};


export function createTaskSession(taskId) {
  const TaskSessionId = 'tmp' + nextTaskSessionId++;
  return {
    type: ActionTypes.TASK_SESSION.CREATE,
    payload: { TaskSessionId, taskId }
  };
};


export function changeCode(TaskSessionId) {
  return {
    type: ActionTypes.TASK_SESSION.CHANGE_CODE,
    payload: { TaskSessionId }
  };
};


export function run(TaskSessionId) {
  return { type: ActionTypes.TASK_SESSION.RUN, TaskSessionId };
};


export function reset(TaskSessionId) {
  return { type: ActionTypes.TASK_SESSION.RESET, TaskSessionId };
};


export function executeCommand(TaskSessionId, command) {
  return { type: ActionTypes.TASK_SESSION.EXECUTE_COMMAND, TaskSessionId, command };
};


export function loadSolution(TaskSessionId) {
  return { type: ActionTypes.TASK_SESSION.LOAD_SOLUTION, TaskSessionId };
};


export function exportCode(TaskSessionId) {
  return { type: ActionTypes.TASK_SESSION.EXPORT_CODE, TaskSessionId };
};
