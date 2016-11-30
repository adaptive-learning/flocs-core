import React from 'react';
import ReactDOM from 'react-dom';
import { SpaceGame } from 'flocs-visual-components';

function handleControlClicked(control) {
  console.log('control:', control);
}

const gameState= {
  fields: [[["b", []], ["b", []], ["b", []]], [["k", ["A"]], ["k", ["S"]], ["k", []]]],
  stage: 'initial'
}
const app = (
  <SpaceGame
    gameState={gameState}
    showCommandControls={true}
    onControlClicked={handleControlClicked}
  />
);
const mountElement = document.getElementById('flocsApp')
ReactDOM.render(app, mountElement);
