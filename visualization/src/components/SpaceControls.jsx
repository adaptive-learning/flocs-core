import React from 'react';


export default class SpaceControls extends React.Component {
  render() {
    return (
      <div>
        <button onClick={this.handleCommandClick.bind(this, 'left')}>Left</button>
        <button onClick={this.handleCommandClick.bind(this, 'ahead')}>Ahead</button>
        <button onClick={this.handleCommandClick.bind(this, 'ahead+shot')}>Ahead+Shot</button>
        <button onClick={this.handleCommandClick.bind(this, 'right')}>Right</button>
      </div>
    );
  };

  handleCommandClick(commandName) {
    this.props.onNewCommand(commandName);
  };
}
