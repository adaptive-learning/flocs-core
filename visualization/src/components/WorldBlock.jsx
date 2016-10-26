import React from 'react';

export default function WorldBlock({ background, objects }) {

  const BACKGROUND_COLOR_CLASSES = {
    'k': '#333',
    'b': '#00f',
  };

  const blockStyle = {
    backgroundColor: BACKGROUND_COLOR_CLASSES[background],
  };

  return (
    <span style={blockStyle}>
      {background}
    </span>
  );
}
