import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getDeck, updateDeck } from "../api";
import Navbar from "../components/Navbar";
import "../styles/EditDeck.css";

const EditDeck = () => {
  const [deck, setDeck] = useState("");
  const [settings, setSettings] = useState({});
  const [newName, setNewName] = useState("");
  const deckId = window.location.pathname.split("/")[2];
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDeck = async () => {
      console.log(deckId);
      try {
        const response = await getDeck(deckId);
        setDeck(response);
        setNewName(response.name);
        setSettings(response.settings);
      } catch (error) {
        console.error("Failed to fetch deck:", error);
      }
    };
    fetchDeck();
  }, [deckId]);

  const handleSettingChange = (settingKey) => {
    setSettings((prevSettings) => ({
      ...prevSettings,
      [settingKey]: !prevSettings[settingKey],
    }));
  };

  const formatSettingKey = (key) => {
    return key
      .replace(/_/g, ' ')
      .replace(/\b\w/g, char => char.toUpperCase());
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateDeck(deckId, newName, settings);
      navigate(`/decks`);
    } catch (error) {
      alert("Failed to update deck:", error);
    }
  };

  return (
    <div className="edit-card-container">
      <Navbar />
      <h1>Edit Deck {deck.name}</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="deckId">Deck Name:</label>
        <input
          type="text"
          id="deckName"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          required
        />
        <label htmlFor="settings">Settings:</label>
        <div className="settings-list">
          {Object.keys(settings).map((settingKey) => (
            <label key={settingKey} className="deck-option">
              <input
                type="checkbox"
                checked={settings[settingKey]}
                onChange={() => handleSettingChange(settingKey)}
              />
              {formatSettingKey(settingKey)}
            </label>
          ))}
        </div>
        <button type="submit">Update Deck</button>
      </form>
    </div>
  );
};

export default EditDeck;
