import React, { useState, useEffect } from "react";
import { getGame, playGame } from "../api";
import { useNavigate } from "react-router-dom";
import "../styles/Game.css";

const Game = () => {
  const [game, setGame] = useState(null);
  const [currentPlayer, setCurrentPlayer] = useState(null);
  const [currentDeck, setCurrentDeck] = useState(null);
  const [currentChallenge, setCurrentChallenge] = useState(null);
  const [currentRound, setCurrentRound] = useState(null);
  const [totalRounds, setTotalRounds] = useState(null);
  const [isHidden, setIsHidden] = useState(true);
  const navigate = useNavigate();
  const gameName = window.location.pathname.split("/")[2];

  const handlePlayGame = async () => {
    const playInfo = await playGame(gameName);
    if (
      !playInfo ||
      !playInfo.hasOwnProperty("challenge") ||
      !playInfo.hasOwnProperty("player")
    ) {
      alert("Game finished");
      navigate("/games-list");
      return;
    }
    setCurrentPlayer(playInfo.player);
    setCurrentChallenge(playInfo.challenge);
    setCurrentRound(playInfo.current_round);
    setTotalRounds(playInfo.total_rounds);
    setIsHidden(playInfo.is_hidden);
    setCurrentDeck(playInfo.deck_name);
  };

  useEffect(() => {
    const fetchGame = async () => {
      try {
        const fetchedGame = await getGame(gameName);
        setGame(fetchedGame);
        console.log("Fetched game:", fetchedGame);
        setCurrentPlayer(fetchedGame.current_player);
        setCurrentChallenge(fetchedGame.current_challenge);
        setCurrentRound(fetchedGame.current_round);
        setTotalRounds(fetchedGame.total_rounds);
        setIsHidden(fetchedGame.current_is_hidden);
        setCurrentDeck(fetchedGame.current_deck_name);
      } catch (error) {
        console.error("Failed to fetch game:", error);
      }
    };
    fetchGame();
  }, []);

  const toggleChallengeVisibility = () => {
    setIsHidden(false);
  };

  return (
    <div className="game-page">
      <button className="back-button" onClick={() => navigate("/games-list")}>
        Go Back
      </button>
      <div className="game-container">
        <h1 className="game-title">Game: {gameName}</h1>
        {(currentRound !== 0 || totalRounds !== 0) && (
          <h1 className="game-title">
            Rounds: {currentRound}/{totalRounds}
          </h1>
        )}
        <h2 className="game-title">Deck: {currentDeck}</h2>
        <h2 className="game-player">{currentPlayer}</h2>
        <div className="game-info">
          {isHidden ? (
            <p
              className="blurred-challenge"
              onClick={toggleChallengeVisibility}
            >
              {currentChallenge}
            </p>
          ) : (
            <p>
              <span>{currentChallenge}</span>
            </p>
          )}
        </div>
        <button className="play-button" onClick={handlePlayGame}>
          Next
        </button>
      </div>
    </div>
  );
};

export default Game;
