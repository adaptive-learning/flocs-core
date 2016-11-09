import React from 'react';


export default class SpaceControls extends React.Component {
  render() {
    return (
      <div>
        <button onClick={this.props.onNewCommand.bind(this, 'left')}>Left</button>
        <button onClick={this.props.onNewCommand.bind(this, 'ahead')}>Ahead</button>
        <button onClick={this.props.onNewCommand.bind(this, 'ahead+shot')}>Ahead+Shot</button>
        <button onClick={this.props.onNewCommand.bind(this, 'right')}>Right</button>
        <button onClick={this.props.onNewCommand.bind(this, 'run')}>Run</button>
        <button onClick={this.props.onNewCommand.bind(this, 'reset')}>Reset</button>
      </div>
    );
  };
}
