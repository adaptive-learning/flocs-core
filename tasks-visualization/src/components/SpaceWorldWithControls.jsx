import React from 'react';
import SpaceWorld from './SpaceWorld';
import SpaceControls from './SpaceControls'


export default function SpaceWorldWithControls({ fields, controls, handleCommand }) {
  return (
    <div>
      <SpaceWorld fields={fields} />
      <SpaceControls controls={controls} onNewCommand={handleCommand} />
    </div>
  );
}
