import React from 'react';
import SpaceWorldWithControls from '../components/SpaceWorldWithControls';


export default class TaskPreview extends React.Component {
  render() {
    const { blocks } = this.props;
    return (
        <SpaceWorldWithControls blocks={blocks} />
    )
  }
};
