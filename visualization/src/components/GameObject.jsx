import React from 'react';
import Image from './Image'

export default function GameObject({ type, size }) {

  const IMAGE_TYPES = {
    'S': 'spaceship',
    'R': 'rock-large',
    'D': 'diamond',
  };


  return (
    <Image imageId={IMAGE_TYPES[type]} width={size} height={size} />
  );
}
