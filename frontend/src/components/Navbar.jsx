import React from "react";
import { Link } from "react-router-dom";
import "../styles/Navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul className="navbar-list">
        <li className="navbar-item">
          <Link to="/games-list" className="navbar-link">
            Games
          </Link>
        </li>
        <li className="navbar-item">
          <Link to="/deck" className="navbar-link">
            Decks
          </Link>
        </li>
        <li className="navbar-item">
          <Link to="/logout" className="navbar-link">
            Logout
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
