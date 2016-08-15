import ActionTypes from './actionTypes';
import flocsDao from '../services/flocsDao';


let nextTaskInstanceId = 0;


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


function shouldFetchTasks(state) {
  return !(state.posts);
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



export function createTaskInstanceIfNotExist(taskId) {
  // TODO: think and refactor (make it readable)
  return function(dispatch, getState) {
    // TODO: does this logic belong here?
    if (!(taskId in getState().openTasks)) {
      dispatch(createTaskInstance(taskId));
    }
  };
};


export function createTaskInstance(taskId) {
  const taskInstanceId = 'tmp' + nextTaskInstanceId++;
  return {
    type: ActionTypes.TASK_INSTANCE.CREATE,
    payload: { taskInstanceId, taskId }
  };
};


export function changeCode(taskInstanceId) {
  return {
    type: ActionTypes.TASK_INSTANCE.CHANGE_CODE,
    payload: { taskInstanceId }
  };
};


export function run(taskInstanceId) {
  return { type: ActionTypes.TASK_INSTANCE.RUN, taskInstanceId };
};


export function reset(taskInstanceId) {
  return { type: ActionTypes.TASK_INSTANCE.RESET, taskInstanceId };
};


export function executeCommand(taskInstanceId, command) {
  return { type: ActionTypes.TASK_INSTANCE.EXECUTE_COMMAND, taskInstanceId, command };
};


export function loadSolution(taskInstanceId) {
  return { type: ActionTypes.TASK_INSTANCE.LOAD_SOLUTION, taskInstanceId };
};


export function exportCode(taskInstanceId) {
  return { type: ActionTypes.TASK_INSTANCE.EXPORT_CODE, taskInstanceId };
};
