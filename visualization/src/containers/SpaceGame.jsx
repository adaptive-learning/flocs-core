import React from 'react';
import SpaceWorld from '../components/SpaceWorld';
import SpaceControls from '../components/SpaceControls'
import flocsDao from '../services/flocsDao';


export default class SpaceGame extends React.Component {

  constructor(props, context) {
    super(props, context);
    this.state = {
      fields: {},
      hero: null,
    };
  };

  // return serialized blocks as a single array
  getBlocks() {
    var blocks = []
    for (var position in this.state.fields) {
      blocks.push({position: position, name: this.state.fields[position].background});
      // TBA: push all objects on this position as well
    }
    if (this.state.hero !== null) {
      var heroPositionKey = this.state.hero.y + '-' + this.state.hero.x;
      blocks.push({position: heroPositionKey, name: 'space-rocket'});
    }
    return blocks;
  }

  componentDidMount() {
    // TODO: use store
    var key = 'zig-zag'
    flocsDao.gettingTaskByKey(key).then(function(task) {
      this.setState({
        fields: task.setting.fields,
        hero: {x: task.setting.start, y: 1}
      });
    }.bind(this));
  }

  handleNewCommand(command) {
    var delta = {ahead: 0, left: -1, right: +1}[command.direction];
    this.setState({
      hero: {
        x: this.state.hero.x + delta,
        y: this.state.hero.y + 1,
      }
    });
  }

  render() {
    return (
      <div>
        <SpaceWorld blocks={this.getBlocks()} />
        <SpaceControls onNewCommand={this.handleNewCommand.bind(this)} />
      </div>
    )
  }
}
