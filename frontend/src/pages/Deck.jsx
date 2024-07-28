import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getDecks } from "../api";
import Navbar from "../components/Navbar";
import "../styles/Deck.css";

const Deck = () => {
  const [decks, setDecks] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDecks = async () => {
      try {
        const fetchedDecks = await getDecks();
        setDecks(fetchedDecks.data.payload);
        console.log("Fetched decks:", fetchedDecks);
      } catch (error) {
        console.error("Failed to fetch decks:", error);
      }
    };
    fetchDecks();
  }, []);

  const handleAddCard = (deckName) => {
    navigate(`/add-card/${deckName}`);
  };

  const handleEditCard = (cardId) => {
    navigate(`/edit-card/${cardId}`);
  };

  return (
      <div className="decks-container">
      <Navbar />
        <h1>Decks</h1>
        {decks.map((deck) => (
          <div key={deck.id} className="deck">
            <h2>{deck.name}</h2>
            <div className="cards-container">
              {deck.cards.map((card) => (
                <div key={card.id} className="card">
                  <p>{card.challenge}</p>
                  <button
                    className="edit-button"
                    onClick={() => handleEditCard(card.id)}
                  >
                    Edit
                  </button>
                </div>
              ))}
              <button
                className="add-card-button"
                onClick={() => handleAddCard(deck.name)}
              >
                Add Card
              </button>
            </div>
          </div>
        ))}
      </div>
  );
};

export default Deck;
