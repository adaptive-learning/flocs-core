import React from 'react';
import SpaceWorld from '../components/SpaceWorld';

export default class SpaceWorldContainer extends React.Component {

  constructor(props, context) {
    super(props, context);
    this.state = {
      background: [
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
      ],
      objects: [
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [2, 0, 2, 3, 2],
        [0, 1, 0, 1, 0],
        [2, 0, 2, 0, 2],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
      ],
      hero: {pos: 3},
      time: 0,
    };
  };

  getBlocks() {
    var blocks = [
      [{background: 1}, {background: 1}, {background: 1}],
      [{background: 0}, {background: 0}, {background: 0}],
      [{background: 0}, {background: 0}, {background: 0}],
      [{background: 0}, {background: 0}, {background: 0}],
    ];
    return blocks;
  }

  componentDidMount() {
    console.log('did mount -> get data from server');
  }

  render() {
    return (
      <SpaceWorld blocks={this.getBlocks()} />
    )
  }
}
