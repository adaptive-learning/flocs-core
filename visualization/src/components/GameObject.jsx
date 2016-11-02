import React from 'react';
import Image from './Image'

export default function GameObject({ type, size }) {

  const IMAGE_TYPES = {
    'S': 'spaceship',
    'A': 'asteroid',
    'M': 'meteoroid',
    'D': 'diamond',
    'explosion': 'explosion',
    'laser': 'laser',
    'laser-start': 'laser-start',
    'laser-end': 'laser-end',
  };


  return (
    <Image imageId={IMAGE_TYPES[type]} width={size} height={size} position='absolute' />
  );
}
