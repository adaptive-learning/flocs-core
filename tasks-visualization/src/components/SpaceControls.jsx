import React from 'react';


export default function SpaceControls({ controls, onNewCommand }) {
  const GROUP = {
    'left': 'commands',
    'right': 'commands',
    'ahead': 'commands',
    'ahead+shot': 'commands',
    'run': 'run',
    'reset': 'reset'
  }

  function visible(controlGroup) {
    return controls[controlGroup] == 'active' || controls[controlGroup] == 'passive';
  }

  function disabled(controlGroup) {
    return controls[controlGroup] == 'passive';
  }

  function conditionallyRenderControlButton(name, label) {
    const controlGroup = GROUP[name];
    if (visible(controlGroup)) {
      return <button disabled={disabled(controlGroup)} onClick={onNewCommand.bind(this, name)}>{label}</button>
    }
  }

  return (
    <div>
      {conditionallyRenderControlButton('left', 'Left')}
      {conditionallyRenderControlButton('ahead', 'Ahead')}
      {conditionallyRenderControlButton('ahead+shot', 'Ahead+Shot')}
      {conditionallyRenderControlButton('right', 'Right')}
      {conditionallyRenderControlButton('run', 'Run')}
      {conditionallyRenderControlButton('reset', 'Reset')}
    </div>
  );
}
