import React from 'react';
import SpaceWorld from './SpaceWorld';
import SpaceControls from './SpaceControls'


export default class SpaceWorldWithControls extends React.Component {

  constructor(props, context) {
    super(props, context);
    // TODO: state should only be a list of applied commands?
    const initialFields = props.task.setting.fields;  // TODO: stop breaking rule of Demeter
    const initialHeroX = props.task.setting.start;
    this.state = {
      fields: initialFields,
      hero: {x: initialHeroX, y: 1},
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
