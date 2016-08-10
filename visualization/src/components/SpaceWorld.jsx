import React from 'react';
import WorldBlock from './WorldBlock'

export default function SpaceWorld({ blocks }) {
  var dimensions = {xMin: 1, xMax: 3, yMin: 1, yMax: 2};

  return (
    <div>
      {blocks.map((block, index) =>
        <div key={index}><WorldBlock name={block.name}/> @ {block.position}</div>
      )}
    </div>
  );
}
