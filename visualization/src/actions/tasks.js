import ActionTypes from './actionTypes';


let nextTaskInstanceId = 0;


export function fetch() {
  return {
    type: ActionTypes.TASKS.FETCH
  };
};


export function open(taskId) {
  const taskInstanceId = 'tmp' + nextTaskInstanceId++;
  return {
    type: ActionTypes.TASK_INSTANCE.OPEN,
    payload: { taskId, taskInstanceId }
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
