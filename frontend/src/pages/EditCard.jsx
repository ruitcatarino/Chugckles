import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getCard, updateCard } from "../api";
import Navbar from "../components/Navbar";
import "../styles/EditCard.css";

const EditCard = () => {
  const [challenge, setChallenge] = useState("");
  const [deck, setDeck] = useState("");
  const cardId = window.location.pathname.split('/')[2];
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCard = async () => {
      try {
        const response = await getCard(cardId);
        setChallenge(response.challenge);
        setDeck(response.deck_name);
      } catch (error) {
        console.error("Failed to fetch card:", error);
      }
    };
    fetchCard();
  }, [cardId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateCard(cardId, challenge);
      navigate(`/decks`);
    } catch (error) {
      alert("Failed to update card:", error);
    }
  };

  return (
    <div className="edit-card-container">
      <Navbar />
      <h1>Edit Card</h1>
      <h2>Deck: {deck}</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="challenge">Challenge:</label>
        <textarea
          id="challenge"
          value={challenge}
          onChange={(e) => setChallenge(e.target.value)}
          required
        />
        <button type="submit">Update Card</button>
      </form>
    </div>
  );
};

export default EditCard;