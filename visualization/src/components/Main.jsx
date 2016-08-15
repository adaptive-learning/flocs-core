import React from 'react';
import Header from './Header'

export default class Main extends React.Component {
  render() {
    const { path } = this.props;
    return (
      <div>
        <Header path={path} />
        {this.props.children}
      </div>
    )
  }
}
