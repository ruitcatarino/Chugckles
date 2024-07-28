import React, { useState, useEffect } from "react";
import { getGames } from "../api";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import "../styles/GameList.css";

const GameList = () => {
  const [games, setGames] = useState([]);
  const navigate = useNavigate();

  const handlePlayGame = (gameName) => {
    navigate(`/game/${gameName}`);
  };

  const handleCreateNewGame = () => {
    navigate("/create-game");
  };

  useEffect(() => {
    const fetchGames = async () => {
      try {
        const fetchedGames = await getGames();
        setGames(fetchedGames.data.payload);
        console.log("Fetched games:", fetchedGames);
      } catch (error) {
        console.error("Failed to fetch games:", error);
      }
    };
    fetchGames();
  }, []);

  return (
    <div>
      <Navbar />
      <div className="game-list-container">
        <h1>Games</h1>
        {games.map((game) => (
          <div key={game.id} className="game-item">
            <h2>{game.name}</h2>
            <p>Status: {game.is_finished ? "Finished" : "In Progress"}</p>
            <p>Decks: {game.decks.map((deck) => deck.name).join(", ")}</p>
            <p>Challenges: {game.challanges.length}</p>
            <p>
              Current Round: {game.current_round} / {game.total_rounds}
            </p>
            <button onClick={() => handlePlayGame(game.name)}>
              {game.is_finished ? "View Game" : "Play Game"}
            </button>
          </div>
        ))}
        <button className="create-game-button" onClick={handleCreateNewGame}>
          Create New Game
        </button>
      </div>
    </div>
  );
};

export default GameList;
