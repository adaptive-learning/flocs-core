import React from 'react';
import SpaceWorldWithControls from '../components/SpaceWorldWithControls';
import CodeEditor from '../components/CodeEditor';


export default class TaskPreview extends React.Component {
  render() {
    const { fields, handleCommand, code, handleCodeChange } = this.props;
    return (
      <div>
        <SpaceWorldWithControls fields={fields} handleCommand={handleCommand} />
        <CodeEditor code={code} onChange={handleCodeChange} />
      </div>
    )
  }
};
