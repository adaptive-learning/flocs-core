// TODO: tests, docs, readability

function gameState(state, taskSessionId, taskId = null) {
  // TODO: optimize if needed
  // TODO: factor out special case handling from normal flow
  let fields = null;
  if (taskSessionId !== null) {
    fields = computeCurrentFields(state, taskSessionId);
  } else if (taskId !== null) {
    fields = state.tasks[taskId];
  } else {
    throw 'Either taskSessionId or taskId must be specified in order to compute game state';
  }
  const spaceship = findSpaceshipPosition(fields);
  const solved = gameSolved(fields, spaceship);
  const dead = isSpaceshipDead(fields, spaceship);
  return { fields, spaceship, solved, dead }
}


function computeCurrentFields(state, taskSessionId) {
  const taskSession = state.taskSessions[taskSessionId];
  const task = state.tasks[taskSession.taskId];
  const fields = runCommands(task.setting.fields, taskSession.commands);
  return fields;
}


function runCommands(fields, commands) {
  return commands.reduce(runCommand, fields);
}


function runCommand(fields, command) {
  const direction = (command == 'ahead+shot') ? 'ahead' : command;
  const shot = (command == 'ahead+shot');
  const fieldsAfterEvolution = performObjectEvolution(fields);
  const fieldsAfterMove = performMove(fieldsAfterEvolution, direction);
  const newFields = (shot) ?  performShot(fieldsAfterMove) : fieldsAfterMove;
  return newFields;
}


function performObjectEvolution(fields) {
  // TODO: factor out 2D map / (world bg+objects map?) into a separate utility function
  const newFields = fields.map(function (row, i) {
    return row.map(function (field, j) {
      let [background, objects] = field;
      const explosion = (objects.indexOf('explosion') > -1);
      const removeAllIfExplosion = objects => (explosion) ? [] : objects;
      const effects = new Set(['laser', 'laser-start', 'laser-end']);
      const removeEffects = objects => objects.filter(obj => !effects.has(obj));
      const evolvedObjects = removeAllIfExplosion(removeEffects(objects));
      return [background, evolvedObjects];
    });
  });
  return newFields;
}


/**
 * Return new 2D fields after move of the spaceship represented as object 'S'.
 * Dicection is one of 'left', 'ahead', 'right'.
 */
function performMove(fields, direction) {
  const oldSpaceshipPosition = findSpaceshipPosition(fields);
  const horizontalShift = {'left': -1, 'ahead': 0, 'right': 1}[direction];
  const newSpaceshipPosition = [oldSpaceshipPosition[0] - 1, oldSpaceshipPosition[1] + horizontalShift];
  const newFields = fields.map(function (row, i) {
    return row.map(function (field, j) {
      let [background, objects] = field;
      if (i == oldSpaceshipPosition[0] && j == oldSpaceshipPosition[1]) {
        objects = [];
      }
      if (i == newSpaceshipPosition[0] && j == newSpaceshipPosition[1]) {
        objects = [...objects, 'S'];
      }
      return [background, objects];
    });
  });
  return newFields;
}


function performShot(fields) {
  const [yStart, x] = findSpaceshipPosition(fields);
  const noObjectAt = y => fields[y][x][1].length == [];
  let yEnd = yStart - 1;
  while (yEnd > 0 && noObjectAt(yEnd)) {
    yEnd--;
  }
  const newFields = fields.map(function (row, i) {
    return row.map(function (field, j) {
      let [background, objects] = field;
      if (j == x) {
        if (i == yStart) {
          objects = ['laser-start', ...objects]
        } else if (yStart > i && i > yEnd) {
          objects = ['laser', ...objects]
        } else if (i == yEnd) {
          objects = objects.map(shootObject);
          objects = ['laser-end', ...objects]
        }
      }
      return [background, objects];
    });
  });
  return newFields;
}


function shootObject(obj) {
  // TODO: improve readability and maintainability
  const shootableObjects = new Set(['M', 'D']);
  const shotObject = (shootableObjects.has(obj)) ? 'explosion' : obj;
  return shotObject;
}


function findSpaceshipPosition(fields) {
  for (let i=0; i<fields.length; i++)  {
    for (let j=0; j<fields[i].length; j++)  {
      const objects = fields[i][j][1];
      if (objects.indexOf('S') >= 0) {
        return [i, j];
      }
    }
  }
}


function gameSolved(fields, spaceship) {
  return lastRowReached(spaceship);
}


function lastRowReached(spaceship) {
  return spaceship[0] == 0;
}


function isSpaceshipDead(fields, spaceship) {
  return outsideWorld(fields, spaceship) || onRock(fields, spaceship);
  return lastRowReached(fields, spaceship);
}


function outsideWorld(fields, position) {
  const [y, x] = position;
  const [minX, maxX] = [0, fields[0].length-1];
  const [minY, maxY] = [0, fields.length-1];
  return (x < minX || x > maxX || y < minY || y > maxY);
}


function onRock(fields, position) {
  const rockObjects = new Set(['M', 'A']);  //TODO: factor out to common world description?)
  const [y, x] = position;
  const objects = fields[y][x][1];
  return objects.some(object => rockObjects.has(object));
}


export default gameState;
