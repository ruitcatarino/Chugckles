import Login from "./pages/Login";
import Register from "./pages/Register";
import Deck from "./pages/Deck";
import ProtectedRoute from "./components/ProtectedRoute";
import GameList from "./pages/GameList";
import Game from "./pages/Game";
import CreateGame from "./pages/CreateGame";
import EditCard from "./pages/EditCard";
import AddCard from "./pages/AddCard";
import AddDeck from "./pages/AddDeck";
import EditDeck from "./pages/EditDeck";
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
          path="/decks"
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
          path="/edit-card/:cardId"
          element={
            <ProtectedRoute>
              <EditCard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/add-card/:deckID"
          element={
            <ProtectedRoute>
              <AddCard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/edit-deck/:deckID"
          element={
            <ProtectedRoute>
              <EditDeck />
            </ProtectedRoute>
          }
        />
        <Route
          path="/add-deck"
          element={
            <ProtectedRoute>
              <AddDeck />
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
