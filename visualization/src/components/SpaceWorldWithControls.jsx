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
        <SpaceWorld setting={this.props.setting} />
        <SpaceControls onNewCommand={this.handleNewCommand.bind(this)} />
      </div>
    )
  }
}
