import React from 'react';
import SpaceWorldWithControls from '../components/SpaceWorldWithControls';


export default class TaskPreview extends React.Component {
  render() {
    const { fields, handleCommand } = this.props;
    return (
        <SpaceWorldWithControls fields={fields} handleCommand={handleCommand} />
    )
  }
};
