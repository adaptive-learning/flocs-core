import React from 'react';
import GameObject from './GameObject'

export default function WorldBlock({ background, objects }) {

  const BACKGROUND_COLOR_CLASSES = {
    'k': '#222',
    'b': '#00f',
    'g': '#ddd',
    'y': '#fe0',
  };

  const fieldSize = 50;

  const fieldStyle = {
    display: 'table-cell',
    position: 'relative',
    borderStyle: 'solid',
    borderColor: '#444',
    borderWidth: '1px',
    width: fieldSize + 'px',
    height: fieldSize + 'px',
    backgroundColor: BACKGROUND_COLOR_CLASSES[background],
  };

  return (
    <span style={fieldStyle}>
      {objects.map((object, index) => <GameObject key={index} type={object} size={fieldSize}/>)}
    </span>
  );
}
