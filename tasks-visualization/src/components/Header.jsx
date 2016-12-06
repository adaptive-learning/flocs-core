import React from 'react';
import { Link } from 'react-router';


export default class Header extends React.Component {
  render() {
    const { path } = this.props;
    return (
      <div>
        { path.map((part, index) =>
            renderPathPart(partsPrefixToPath(path, index), part, index)) }
      </div>
    )
  }
}


function renderPathPart(path, name, index) {
  return (
    <span key={index}>
    /&nbsp;
    <Link to={path}>{name}</Link>
    &nbsp;
    </span>
  );
}


function partsPrefixToPath(allParts, count) {
  const prefixParts = allParts.slice(1, count+1);
  const path = '/' + prefixParts.join('/');
  return path;
}
