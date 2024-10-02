// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Form Page</Link>
        </li>
        <li>
          <Link to="/response">Response Page</Link>
        </li>
        {/* Add more links as needed */}
      </ul>
    </nav>
  );
};

export default Navbar;
