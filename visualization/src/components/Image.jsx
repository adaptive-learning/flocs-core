import React from 'react';

export default function Image({ imageId, width, height, position }) {

  const imageStyle = {
    width: width + 'px',
    height: height + 'px',
    position: position || 'relative',
  };

  const sourcePath = `/img/${imageId}.png`

  return (
    <img src={sourcePath} style={imageStyle} />
  );
}
