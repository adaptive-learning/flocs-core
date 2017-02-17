/* Convert robocode to JSON */
/* run by node ./scripts/parse_robocode.js */
/*
TODO:
- checks (?)
- make it more readable (separate grammar specification from parsing algorithm),
  possibly use some 3rd party parsing library
- nested condtions, if-else statements
- unit tests

Grammar:
PROGRAM -> SEQ
SEQ -> CMD | CMD \n SEQ
CMD -> MOVE | WHILE | REPEAT | (...)
MOVE -> move() | move('ahead') | move('left') | move('right')
WHILE -> while COND: \n{ SEQ }  # { and } denotes indentation change
REPEAT -> repeat COND: \n{ SEQ }
COND -> COND and COND | COND or COND | VAL REL VAL
VAL -> COLOR | NUM
COLOR -> color() | 'b' | 'r' | 'y' | 'k'
NUM -> position() | 1 | 2 | 3 | 4 | 5
REL -> == | != | > | >= | < | <=
*/
const readline = require('readline');


function parseRobocode(text) {
  let lines = textToNonemptyIndentedLines(text);
  let program = parseNonemptyIndentedLines(lines);
  return program;
}


function textToNonemptyIndentedLines(text) {
  let lines = text.split(/\n/);
  let indentedLines = lines.map(function(line) {
    let spacesCount = line.search(/\S|$/);
    return [spacesCount, line.trim()];
  });
  let nonemptyIndentedLines = indentedLines.filter(indLine => indLine[1].length > 0);
  return nonemptyIndentedLines;
}


function parseNonemptyIndentedLines(lines) {
  let nestedLines = nestIndentedLines(lines);
  let program = parseSequence(nestedLines);
  return program;
}


function parseSequence(nestedLines) {
  return nestedLines.map(parseCommand);
}


function parseCommand({head, body}) {
  if (head.startsWith('move')) {
    // TODO: force empty body
    return parseMove(head);
  } else if (head.startsWith('while')) {
    return ['while', parseCondition(head.slice(6)), parseSequence(body)];
  } else if (head.startsWith('repeat')) {
    return ['repeat', parseNumber(head.slice(6)), parseSequence(body)];
  } else if (head.startsWith('if')) {
    return ['if', parseCondition(head.slice(3)), parseSequence(body)];
  } else {
    throw `Uknown command: ${head}`
  }
}


function parseNumber(text) {
  const numberRe = /(\d+)/;
  const match = numberRe.exec(text);
  const number = parseInt(match[1]);
  return number;
}


function parseMove(line) {
  var moveCmdRe = /^move\((['"](.*)['"])?\)$/;
  var match = moveCmdRe.exec(line);
  var direction = match[2] || 'ahead';
  return ['move', direction];
}


function parseCondition(line) {
  // TODO: allow for nested conditions
  //return alternatives(simpleCondition, andCondition, orCondition)(line);
  if (line.indexOf(' and ') >= 0) {
    return parseAndCondition(line);
  } else if (line.indexOf(' or ') >= 0) {
    return parseOrCondition(line);
  } else {
    return parseSimpleCondition(line);
  }
}


function parseSimpleCondition(text) {
  const tokens = tokenize(text);
  const conditionParser = {
    color: parseColorCondition,
    position: parsePositionCondition,
  }[tokens[0]];
  const condition = conditionParser(tokens);
  return condition;
}


function tokenize(line) {
  const tokens = line.split(/[ ()'"]+/);
  return tokens;
}


function parseColorCondition(tokens) {
  const op = tokens[1];
  const color = tokens[2];
  // TODO: checks and error reports
  return ['color', op, color];
}


function parsePositionCondition(tokens) {
  const op = tokens[1];
  const position = parseInt(tokens[2]);
  // TODO: checks and error reports
  return ['position', op, position];
}


function parseAndCondition(text) {
  const parts = text.split(' and ');
  return ['and', parseSimpleCondition(parts[0]), parseSimpleCondition(parts[1])];
}


function parseOrCondition(text) {
  const parts = text.split(' or ');
  return ['or', parseSimpleCondition(parts[0]), parseSimpleCondition(parts[1])];
}


function nestIndentedLines(lines) {
  let nestedLines = [];
  let openSequences = [nestedLines];
  for (const [indentation, line] of lines) {
    if (indentation % 4 != 0) {
      throw 'Expects indentation to be multiple of 4.';
    }
    const level = indentation / 4;
    if (level <= openSequences.length) {
      openSequences.length = level + 1;
      const newNode = {head: line, body: []}
      openSequences[level].push(newNode);
      openSequences.push(newNode.body);
    } else {
      throw `Unexpectedly large indentation ${indentation}`;
    }
  }
  return nestedLines;
}


AVAILABLE_COLORS = {
  b: 'blue',
  r: 'red',
  y: 'yellow',
  k: 'black',
}


AVAILABLE_DIRECTIONS = {
  a: 'ahead',
  l: 'left',
  r: 'right',
}


AVAILABLE_POSITIONS = {
  left: 1,
  right: 5,
}


//const test = `
//move()
//while color() != 'b':
//    move('right')
//    move('left')

const test = `
move()
if position() > 4:
    repeat(4):
        move('right')
        move('left')
`

//console.log(JSON.stringify(parseRobocode(test)));
//console.log(parseRobocode(test)[1].body);
//console.log(parseMove('move()'));

process.stdin.on('data', function(buffer) {
  const text = buffer.toString();
  const ast = parseRobocode(text);
  console.log(JSON.stringify(ast));
});
