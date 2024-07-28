import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api';
import "../styles/Form.css"
import logo from '../assets/logo.png';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      if (username.length === 0 || password.length === 0) {
        alert('Please fill in all fields');
        return;
      }
      try {
        const token = await login(username, password);
        localStorage.setItem('token', token);
        navigate('/games-list');
      } catch (error) {
        alert('Login failed: ' + error);
      }
    };

    const handleRegister = async (e) => {
      e.preventDefault();
      navigate('/register');
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
        <div className="form-buttons">
          <button type="submit" className="login-button">
            Login
          </button>
          <button onClick={handleRegister} className="register-button">
            Register
          </button>
        </div>
      </form>
    );
  };
  
  export default Login;