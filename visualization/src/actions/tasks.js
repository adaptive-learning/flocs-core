import ActionTypes from './actionTypes';
import { Interpreter } from 'js-interpreter/interpreter';


let nextTaskSessionId = 0;


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
  const taskSessionId = 'tmp' + nextTaskSessionId++;
  return {
    type: ActionTypes.TASK_SESSION.CREATE,
    payload: { taskSessionId, taskId }
  };
};


export function changeCode(taskSessionId) {
  return {
    type: ActionTypes.TASK_SESSION.CHANGE_CODE,
    payload: { taskSessionId }
  };
};


export function runProgram(taskSessionId) {
  // QUESTION: should this code be here?
  // QUESTION: how to make it readable?
  return function(dispatch, getState) {
    const program = getState().taskSessions[taskSessionId].program;
    // TODO: factor out to a RoboCodeInterpreter
    const jsCode = roboAstToJS(program);
    let pause = false;

    function initApi(interpreter, scope) {
      interpreter.setProperty(scope, 'move',
        interpreter.createNativeFunction(function(direction) {
          direction = direction ? direction.toString() : 'ahead';
          move(direction);
          pause = true;
          return interpreter.createPrimitive();
      }));
    }

    function move(direction) {
      // TODO: unify naming for commands/moves/directions
      dispatch(executeCommand(taskSessionId, direction));
    };

    var jsInterpreter = new Interpreter(jsCode, initApi);

    // running in interpreter - stepping with delays
    const PAUSE_LENGTH = 500; // TODO: use settings part of the state for pause length
    function nextStep() {
      let ok = true;
      while (ok && !pause) {
        ok = jsInterpreter.step();
      }
      if (ok) {
        pause = false;
        window.setTimeout(nextStep, PAUSE_LENGTH);
      }
    }
    nextStep();
    // TODO: first run the program (then stepping with delay)
    //dispatch(createTaskSession(taskId));
  };
};


// QUESTION: where should this code live?
function roboAstToJS(roboAst) {
  // TODO: unfake it
  // TODO: unable to highlight lines(/blocks)
  //const jsCode = 'move()\nmove("right")\nmove()\n';
  const lines = roboAst.map(function(node) {
    switch (node[0]) {
      case 'move':
        const [command, ...args] = node;
        const argsList = args.map(encodeArgument).join(',');
        return `${command}(${argsList})`;
    };
  });
  // TODO: define all other robo-code supported constructs (see robo-code spec)
  const jsCode = lines.join('\n');
  console.log('program:', jsCode);
  return jsCode;
}


// TODO: test
function encodeArgument(arg) {
  if (typeof arg == 'string') {
    return `"${arg}"`;
  } else {
    return arg;
  };
}



export function resetWorld(taskSessionId) {
  return {
    type: ActionTypes.TASK_SESSION.RESET,
    payload: { taskSessionId }
  };
};


export function executeCommand(taskSessionId, commandName) {
  return {
    type: ActionTypes.TASK_SESSION.EXECUTE_COMMAND,
    payload: { taskSessionId, commandName }
  };
};
