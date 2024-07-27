import Login from './pages/Login';
import ProtectedRoute from './components/ProtectedRoute';
import {BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

function Logout() {
  localStorage.clear();
  return <Navigate to="/" />
}

function NotFound() {
  return <Navigate to="/" />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/games" element={<ProtectedRoute></ProtectedRoute>} />
        <Route path="/logout" element={<ProtectedRoute><Logout /></ProtectedRoute>} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App
