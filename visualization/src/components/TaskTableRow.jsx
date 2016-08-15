import React from 'react';
import { Link } from 'react-router';


export default class TaskTableRow extends React.Component {
  render() {
    const { task } = this.props;
    return (
      <tr>
        <td>{ task.id }</td>
        <td><Link to={`/task/${task.id}`}>{ task.ref }</Link></td>
      </tr>
    )
  }
};
