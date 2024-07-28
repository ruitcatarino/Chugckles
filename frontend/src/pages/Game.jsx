import React, { useState, useEffect } from 'react';
import { getGame, playGame } from '../api';
import { useNavigate } from 'react-router-dom';
import "../styles/GameList.css";

const Game = () => {
    const [game, setGame] = useState(null);
    const [currentPlayer, setCurrentPlayer] = useState(null);
    const [currentChallenge, setCurrentChallenge] = useState(null);
    const navigate = useNavigate();
    const gameName = window.location.pathname.split('/')[2];

    const handlePlayGame = async () => {
        const playInfo = await playGame(gameName);
        if (!playInfo || !playInfo.hasOwnProperty('challange') || !playInfo.hasOwnProperty('player')) {
            alert('Game finished');
            navigate('/games-list');
            return;
        }
        setCurrentPlayer(playInfo.challange);
        setCurrentChallenge(playInfo.player);
    };

    useEffect(() => {
        const fetchGame = async () => {
            try {
                const fetchedGame = await getGame(gameName);
                setGame(fetchedGame);
                console.log("Fetched game:", fetchedGame);
                setCurrentPlayer(fetchedGame.current_player);
                setCurrentChallenge(fetchedGame.current_challange);
            } catch (error) {
                console.error("Failed to fetch game:", error);
            }   
        };
        fetchGame();
    }, []);

    return (
        <div className="game-container">
            <h1>{game?.name}</h1>
            <p>Current Player: {currentPlayer}</p>
            <p>Current Challenge: {currentChallenge}</p>
            <button onClick={handlePlayGame}>Play Game</button>
        </div>
    );
};

export default Game;