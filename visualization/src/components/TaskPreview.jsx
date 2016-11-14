import React from 'react';
import TaskStatus from '../components/TaskStatus';
import SpaceWorldWithControls from '../components/SpaceWorldWithControls';
import CodeEditor from '../components/CodeEditor';


export default class TaskPreview extends React.Component {
  render() {
    const { fields, initial, solved, dead, handleCommand, code, handleCodeChange } = this.props;
    const controls = {
      commands: (solved || dead) ? 'passive' : 'active',
      run: initial ? 'active' : 'hidden',
      reset: (!initial) ? 'active' : 'hidden'
    };
    return (
      <div>
        <TaskStatus solved={solved} dead={dead} />
        <SpaceWorldWithControls controls={controls} fields={fields} handleCommand={handleCommand} />
        <CodeEditor code={code} onChange={handleCodeChange} />
      </div>
    )
  }
};
