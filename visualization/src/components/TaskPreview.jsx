import React from 'react';
import TaskStatus from '../components/TaskStatus';
import SpaceWorldWithControls from '../components/SpaceWorldWithControls';
import CodeEditor from '../components/CodeEditor';


export default class TaskPreview extends React.Component {
  render() {
    const { fields, solved, dead, handleCommand, code, handleCodeChange } = this.props;
    return (
      <div>
        <TaskStatus solved={solved} dead={dead} />
        <SpaceWorldWithControls fields={fields} handleCommand={handleCommand} />
        <CodeEditor code={code} onChange={handleCodeChange} />
      </div>
    )
  }
};
