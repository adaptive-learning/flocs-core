/* Convert robocode to JSON */
/* run by node ./scripts/parse_robocode.js */

function robocodeToJson(text) {
  let lines = text.split(/\n/);
  let indentedLines = lines.map(function(line) {
    let spacesCount = line.search(/\S|$/);
    return [spacesCount, line.trim()];
  });
  let nonemptyIndentedLines = indentedLines.filter(indLine => indLine[1].length > 0);
  var json = nonemptyIndentedLines;
  return json;
}


const test = `
move()
while color() != 'b':
    move('right')
    move('left')
`
console.log(robocodeToJson(test));
