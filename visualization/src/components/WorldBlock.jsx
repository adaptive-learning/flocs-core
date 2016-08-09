import React from 'react';

export default function WorldBlock(props) {
  var {background, object} = props.data;
  return (
    <span>
      [{background}]
    </span>
  );
}
