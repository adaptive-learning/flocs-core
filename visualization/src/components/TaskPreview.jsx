import React from 'react';
import SpaceWorldWithControls from '../components/SpaceWorldWithControls';


export default class TaskPreview extends React.Component {
  render() {
    const { task } = this.props;
    return (
        <SpaceWorldWithControls setting={task.setting} />
    )
  }
};
