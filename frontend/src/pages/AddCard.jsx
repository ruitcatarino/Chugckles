import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { createCard, getDeck } from "../api";
import Navbar from "../components/Navbar";
import "../styles/AddCard.css";

const AddCard = () => {
  const [challenge, setChallenge] = useState("");
  const [deck, setDeck] = useState("");
  const deckId = window.location.pathname.split("/")[2];
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDeck = async () => {
      try {
        const response = await getDeck(deckId);
        setDeck(response);
      } catch (error) {
        console.error("Failed to fetch deck:", error);
      }
    };
    fetchDeck();
  }, [deckId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createCard(deckId, challenge);
      navigate(`/decks`);
    } catch (error) {
      alert("Failed to add card:", error);
    }
  };

  return (
    <div className="add-card-container">
      <Navbar />
      <h1>Add Card to {deck.name}</h1>
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
