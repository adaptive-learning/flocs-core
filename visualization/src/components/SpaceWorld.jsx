import React from 'react';
import WorldBlock from '../components/WorldBlock'

export default function SpaceWorld(props) {
  var dimensions = {xMin: 1, xMax: 3, yMin: 1, yMax: 2};

  return (
    <div>
      {props.blocks.map((block, index) =>
        <div key={index}><WorldBlock name={block.name}/> @ {block.position}</div>
      )}
    </div>
  );
}
