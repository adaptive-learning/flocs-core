import React from 'react';
import { Link } from 'react-router';

export default function Home(props) {
  return (
    <div>
      <p>
        Static data preview:
      </p>
      <ul>
        <li><Link to='/tasks'>Tasks</Link></li>
      </ul>
    </div>
  )
}
