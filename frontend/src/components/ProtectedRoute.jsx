import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { useEffect, useState } from "react";

function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    auth().catch(() => setIsAuthenticated(false));
  }, []);

  const auth = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setIsAuthenticated(false);
      return;
    }
    const tokenDecoded = jwtDecode(token);
    const tokenExpiration = tokenDecoded.exp;

    if (tokenExpiration * 1000 < Date.now()) {
      localStorage.removeItem("token");
      setIsAuthenticated(false);
      return;
    } else {
      setIsAuthenticated(true);
      return;
    }
  };

  if (isAuthenticated === null) {
    return <div>Loading...</div>;
  }

  return isAuthenticated ? children : <Navigate to="/" />;
}

export default ProtectedRoute;
