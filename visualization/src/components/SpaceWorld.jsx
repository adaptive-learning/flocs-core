import React from 'react';
import WorldBlock from './WorldBlock'

export default function SpaceWorld({ setting }) {
  //var dimensions = {xMin: 1, xMax: 3, yMin: 1, yMax: 2};
  //console.log(setting.fields);
  const { fields } = setting;

  return (
    <div>
      {fields.map((fieldRow, index) =>
        <div key={index}>
        {fieldRow.map((field, index) =>
          <WorldBlock key={index} background={field[0]} objects={field[1]}/>
        )}
        </div>
      )}
    </div>
  );
}
