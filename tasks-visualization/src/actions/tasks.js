import ActionTypes from './actionTypes';
import { Interpreter } from 'js-interpreter/interpreter';
import gameState from '../extractors/gameState';
import parseRobocode from '../robocode/parser';


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


export function changeCode(taskSessionId, code) {
  return {
    type: ActionTypes.TASK_SESSION.CHANGE_CODE,
    payload: { taskSessionId, code }
  };
};


export function runProgram(taskSessionId) {
  // QUESTION: should this code be here?
  // QUESTION: how to make it readable?
  return function(dispatch, getState) {
    const code = getState().taskSessions[taskSessionId].code;
    const roboAst = parseRobocode(code);
    // TODO: factor out to a RoboCodeInterpreter
    const jsCode = roboAstToJS(roboAst);
    let pause = false;

    function initApi(interpreter, scope) {
      // TODO: dry initApi function
      interpreter.setProperty(scope, 'move',
        interpreter.createNativeFunction(function(direction) {
          direction = direction ? direction.toString() : 'ahead';
          move(direction);
          pause = true;
          return interpreter.createPrimitive();
      }));

      interpreter.setProperty(scope, 'color',
        interpreter.createNativeFunction(function() {
          return interpreter.createPrimitive(readColor());
      }));

      interpreter.setProperty(scope, 'position',
        interpreter.createNativeFunction(function() {
          return interpreter.createPrimitive(readPosition());
      }));
    }

    function move(direction) {
      // TODO: unify naming for commands/moves/directions
      dispatch(executeCommand(taskSessionId, direction));
    };

    function readColor() {
      const { fields, spaceship } = gameState(getState(), taskSessionId);
      const field = fields[spaceship[0]][spaceship[1]];  // TODO: better way to index fields in 2d map?
      const color = field[0];  // TODO: more explicit way to get background
      return color;
    }

    function readPosition() {
      const { spaceship } = gameState(getState(), taskSessionId);
      const [y, x] = spaceship;
      const position = x + 1;
      return position;
    }

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
// TODO: documentation and tests
function roboAstToJS(roboAst) {
  // TODO: enable to highlight lines(/blocks)
  const jsCode = generateSequence(roboAst);
  console.log('program:', jsCode);
  return jsCode;
}


function generateSequence(nodes) {
  const lines = nodes.map(generateStatement);
  const jsCode = lines.join('\n');
  return jsCode;
}


function generateStatement(node) {
  const head = node[0];
  switch (head) {
    case 'move':
      return generateCommand(node);
    case 'repeat':
      return generateRepeatLoop(node);
    case 'while':
      return generateWhileLoop(node);
    case 'if':
      return generateIfStatement(node);
    default:
      throw `Unknown node head in roboAST <${head}> in node <${node}> for statement`
  };
}

function generateCommand(node) {
  const [command, ...args] = node;
  const argsList = args.map(encodeValue).join(',');
  return `${command}(${argsList})`;
}


function generateRepeatLoop(node) {
  const [_, count, body] = node;
  const bodyCode = generateSequence(body);
  return `for (var i=0; i<${count}; i++) {\n${bodyCode}\n}`;
}


function generateWhileLoop(node) {
  const [_, condition, body] = node;
  const conditionCode = generateCondition(condition);
  const bodyCode = generateSequence(body);
  return `while ${conditionCode} {\n${bodyCode}\n}`;
}


function generateIfStatement(node) {
  const [_, condition, body] = node;
  const conditionCode = generateCondition(condition);
  const bodyCode = generateSequence(body);
  return `if ${conditionCode} {\n${bodyCode}\n}`;
}


function generateCondition(node) {
  const head = node[0];
  switch (head) {
    case 'color':
    case 'position':
      return generateSimpleCondition(node);
    case 'and':
      return generateComplexCondition('&&', node[1], node[2]);
    case 'or':
      return generateComplexCondition('||', node[1], node[2]);
    default:
      throw `Unknown node head in roboAST <${head}> in node <${node}> for condition`
  };
}


function generateSimpleCondition(node) {
  const [fnName, comparator, value] = node;
  return `(${fnName}() ${comparator} ${encodeValue(value)})`;
}


function generateComplexCondition(operator, leftConditionNode, rightConditionNode) {
  const leftCondition = generateSimpleCondition(leftConditionNode);
  const rightCondition = generateSimpleCondition(rightConditionNode);
  return `(${leftCondition} ${operator} ${rightCondition})`;
}


// TODO: test
function encodeValue(arg) {
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
