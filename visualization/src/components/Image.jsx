import React from 'react';

export default function Image({ imageId, width, height }) {

  const imageStyle = {
    width: width + 'px',
    height: height + 'px',
  };

  const sourcePath = `/img/${imageId}.png`

  return (
    <img src={sourcePath} style={imageStyle} />
  );
}
