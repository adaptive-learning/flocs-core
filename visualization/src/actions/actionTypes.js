// TODO: unify naming conventions (use a style-guide), e.g. ActionTypes vs. actionTypes
const ActionTypes = {
  TASKS: {
    REQUEST: 'REQUEST TASKS',
    RECEIVE: 'RECEIVE TASKS',
    //OPEN: 'OPEN TASK',
  },
  TASK_INSTANCE: {
    CREATE: 'CREATE TASK INSTANCE',
    CHANGE_CODE: 'CHANGE CODE IN TASK INSTANCE',
    RUN: 'RUN TASK INSTANCE',
    EXECUTE_COMMAND: 'EXECUTE COMMAND IN TASK INSTANCE',
    RESET: 'RESET TASK INSTANCE',
    LOAD_SOLUTION: 'LOAD SOLUTION OF TASK INSTANCE',
    EXPORT_CODE: 'EXPORT CODE OF TASK INSTANCE',
  }
};

export default ActionTypes;