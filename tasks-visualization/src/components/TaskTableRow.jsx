import React from 'react';
import { Link } from 'react-router';


export default class TaskTableRow extends React.Component {
  render() {
    const { task } = this.props;
    return (
      <tr>
        <td><Link to={`/tasks/${task.taskId}`}>{ task.taskId }</Link></td>
      </tr>
    )
  }
};
