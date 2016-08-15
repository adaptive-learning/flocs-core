import React from 'react';
import TaskTableRow from './TaskTableRow'


export default class TaskTable extends React.Component {
  render() {
    const { tasks } = this.props;
    const sortedIds = Object.keys(tasks).sort();
    return (
      <table>
        <tbody>
        { sortedIds.map(id => <TaskTableRow key={id} task={tasks[id]}/>) }
        </tbody>
      </table>
    )
  }
};
