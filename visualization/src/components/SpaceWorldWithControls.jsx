import React from 'react';
import SpaceWorld from './SpaceWorld';
import SpaceControls from './SpaceControls'


export default class SpaceWorldWithControls extends React.Component {

  render() {
    return (
      <div>
        <SpaceWorld fields={this.props.fields} />
        <SpaceControls onNewCommand={this.props.handleCommand} />
      </div>
    )
  }
}
