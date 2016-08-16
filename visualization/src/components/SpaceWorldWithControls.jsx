import React from 'react';
import SpaceWorld from './SpaceWorld';
import SpaceControls from './SpaceControls'


export default class SpaceWorldWithControls extends React.Component {

  handleNewCommand(command) {
    // TBA
    console.log('command:', command);
  }

  render() {
    return (
      <div>
        <SpaceWorld blocks={this.props.blocks} />
        <SpaceControls onNewCommand={this.handleNewCommand.bind(this)} />
      </div>
    )
  }
}
