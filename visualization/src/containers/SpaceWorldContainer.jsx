import React from 'react';
import SpaceWorld from '../components/SpaceWorld';

export default class SpaceWorldContainer extends React.Component {

  constructor(props, context) {
    super(props, context);
    this.state = {
      hero: "{TBA: x-y}"
    };
  };

  render() {
    return (
      <SpaceWorld
        hero={this.state.hero}
      />
    )
  }
}
