import React from 'react';
import WorldBlock from '../components/WorldBlock'

export default function SpaceWorld(props) {
  return (
    <div>
      {props.blocks.map((row, index) =>
        <SpaceWorldRow key={index} blocks={row}/>
      )}
    </div>
  );
}


function SpaceWorldRow(props) {
  return (
    <div>
      {props.blocks.map((block, index) =>
        <WorldBlock key={index} data={block}/>
      )}
    </div>
  );
}

