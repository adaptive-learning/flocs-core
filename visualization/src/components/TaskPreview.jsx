import React from 'react';


export default class TaskPreview extends React.Component {
  render() {
    return (
      <div>
        TBA: task {this.props.params.taskId}
      </div>
    )
  }
};
