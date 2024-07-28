import Login from "./pages/Login";
import Register from "./pages/Register";
import Deck from "./pages/Deck";
import ProtectedRoute from "./components/ProtectedRoute";
import GameList from "./pages/GameList";
import Game from "./pages/Game";
import CreateGame from "./pages/CreateGame";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

function Logout() {
  localStorage.clear();
  return <Navigate to="/" />;
}

function NotFound() {
  return <Navigate to="/" />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/deck"
          element={
            <ProtectedRoute>
              <Deck />
            </ProtectedRoute>
          }
        />
        <Route
          path="/games-list"
          element={
            <ProtectedRoute>
              <GameList />
            </ProtectedRoute>
          }
        />
        <Route
          path="/game/:gameName"
          element={
            <ProtectedRoute>
              <Game />
            </ProtectedRoute>
          }
        />
        <Route
          path="/create-game"
          element={
            <ProtectedRoute>
              <CreateGame />
            </ProtectedRoute>
          }
        />
        <Route
          path="/logout"
          element={
            <ProtectedRoute>
              <Logout />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
