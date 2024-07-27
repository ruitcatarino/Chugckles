import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { register } from '../api';
import "../styles/Form.css"
import logo from '../assets/logo.png';

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [passwordConfirm, setPasswordConfirm] = useState('');
    const navigate = useNavigate();
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      if (password !== passwordConfirm) {
        alert('Passwords do not match');
        return;
      }
      try {
        await register(username, password);
        navigate('/');
      } catch (error) {
        alert('Register failed: ' + error);
      }
    };
  
    return (
      <form onSubmit={handleSubmit} className="form-container">
        <img src={logo} alt="Logo"/>
        <input
          type="text"
          className="form-input"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />
        <input
          className="form-input"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        <input
          className="form-input"
          type="password"
          value={passwordConfirm}
          onChange={(e) => setPasswordConfirm(e.target.value)}
          placeholder="Confirm Password"
        />
        <div className="form-buttons">
        <button type="submit" className="register-button">
            Register
          </button>
        </div>
      </form>
    );
  };
  
  export default Register;