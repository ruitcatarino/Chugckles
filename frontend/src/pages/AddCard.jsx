import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createCard } from "../api";
import Navbar from "../components/Navbar";
import "../styles/AddCard.css";

const AddCard = () => {
  const [challenge, setChallenge] = useState("");
  const deckName = window.location.pathname.split('/')[2];
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createCard(deckName, challenge);
      navigate(`/decks`);
    } catch (error) {
      alert("Failed to add card:", error);
    }
  };

  return (
    <div className="add-card-container">
      <Navbar />
      <h1>Add Card to {deckName}</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="challenge">Challenge:</label>
        <textarea
          id="challenge"
          value={challenge}
          onChange={(e) => setChallenge(e.target.value)}
          required
        />
        <button type="submit">Add Card</button>
      </form>
    </div>
  );
};

export default AddCard;