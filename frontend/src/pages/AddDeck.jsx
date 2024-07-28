import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createDeck } from "../api";
import Navbar from "../components/Navbar";
import "../styles/AddDeck.css";

const AddDeck = () => {
  const [deckName, setDeckName] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createDeck(deckName);
      navigate("/decks");
    } catch (error) {
      console.error("Failed to add deck:", error);
    }
  };

  return (
    <div className="add-deck-container">
      <Navbar />
      <h1>Add New Deck</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="deckName">Deck Name:</label>
        <input
          type="text"
          id="deckName"
          value={deckName}
          onChange={(e) => setDeckName(e.target.value)}
          required
        />
        <button type="submit">Add Deck</button>
      </form>
    </div>
  );
};

export default AddDeck;
