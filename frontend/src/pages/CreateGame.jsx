import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getDecks, createGame } from "../api";
import Navbar from "../components/Navbar";
import "../styles/CreateGame.css";

const CreateGame = () => {
  const [gameName, setGameName] = useState("");
  const [selectedDecks, setSelectedDecks] = useState([]);
  const [rounds, setRounds] = useState(10);
  const [availableDecks, setAvailableDecks] = useState([]);
  const [players, setPlayers] = useState([""]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDecks = async () => {
      try {
        const fetchedDecks = await getDecks();
        setAvailableDecks(fetchedDecks.data.payload);
      } catch (error) {
        console.error("Failed to fetch decks:", error);
      }
    };
    fetchDecks();
  }, []);

  const handleDeckToggle = (deckName) => {
    setSelectedDecks((prev) =>
      prev.includes(deckName)
        ? prev.filter((name) => name !== deckName)
        : [...prev, deckName]
    );
  };

  const handlePlayerChange = (index, value) => {
    const newPlayers = [...players];
    newPlayers[index] = value;
    setPlayers(newPlayers);
  };

  const addPlayer = () => {
    setPlayers([...players, ""]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (
      !gameName ||
      selectedDecks.length === 0 ||
      players.filter((p) => p.trim()).length === 0
    ) {
      alert(
        "Please enter a game name, select at least one deck, and add at least one player."
      );
      return;
    }

    try {
      const message = await createGame(
        gameName,
        selectedDecks,
        players.filter((p) => p.trim()),
        rounds
      );
      navigate(`/games-list`);
    } catch (error) {
      console.error("Error creating game:", error);
      alert("Failed to create game. " + error);
    }
  };

  return (
    <div className="create-game-container">
      <Navbar />
      <h1>Create New Game</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="gameName">Game Name:</label>
          <input
            type="text"
            id="gameName"
            value={gameName}
            onChange={(e) => setGameName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Select Decks:</label>
          <div className="deck-list">
            {availableDecks.map((deck) => (
              <label key={deck.name} className="deck-option">
                <input
                  type="checkbox"
                  checked={selectedDecks.includes(deck.name)}
                  onChange={() => handleDeckToggle(deck.name)}
                />
                {deck.name}
              </label>
            ))}
          </div>
        </div>
        <div className="form-group">
          <label>Players:</label>
          {players.map((player, index) => (
            <input
              key={index}
              type="text"
              value={player}
              onChange={(e) => handlePlayerChange(index, e.target.value)}
              placeholder={`Player ${index + 1}`}
            />
          ))}
          <button type="button" onClick={addPlayer}>
            Add Player
          </button>
        </div>
        <div className="form-group">
          <label htmlFor="rounds">Number of Rounds:</label>
          <input
            type="number"
            id="rounds"
            value={rounds}
            onChange={(e) => setRounds(Math.max(1, parseInt(e.target.value)))}
            min="1"
            required
          />
        </div>
        <button type="submit" className="create-button">
          Create Game
        </button>
      </form>
    </div>
  );
};

export default CreateGame;
