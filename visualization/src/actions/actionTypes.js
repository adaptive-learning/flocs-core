// TODO: unify naming conventions (use a style-guide), e.g. ActionTypes vs. actionTypes
const ActionTypes = {
  TASKS: {
    REQUEST: 'REQUEST TASKS',
    RECEIVE: 'RECEIVE TASKS',
    //OPEN: 'OPEN TASK',
  },
  TASK_SESSION: {
    CREATE: 'CREATE TASK SESSION',
    CHANGE_CODE: 'CHANGE CODE IN TASK SESSION',
    RUN: 'RUN TASK SESSION',
    EXECUTE_COMMAND: 'EXECUTE COMMAND IN TASK SESSION',
    RESET: 'RESET TASK SESSION',
    LOAD_SOLUTION: 'LOAD SOLUTION OF TASK SESSION',
    EXPORT_CODE: 'EXPORT CODE OF TASK SESSION',
  }
};

export default ActionTypes;
