import React from 'react';
import WorldBlock from './WorldBlock'

export default function SpaceWorld({ fields }) {
  return (
    <div>
      {fields.map((fieldRow, index) =>
        <span style={{display: 'table-row'}} key={index}>
        {fieldRow.map((field, index) =>
          <WorldBlock key={index} background={field[0]} objects={field[1]}/>
        )}
        </span>
      )}
    </div>
  );
}
