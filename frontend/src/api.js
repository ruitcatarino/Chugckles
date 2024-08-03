import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://backend:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

export const login = async (username, password) => {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);
  try {
    const response = await axios.post(
      `${API_URL}/user/login`,
      formData.toString(),
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );
    return response.data.token;
  } catch (error) {
    throw error.response.data.detail;
  }
};

export const register = async (username, password) => {
  try {
    const response = await api.post("/user/register", {
      username,
      password,
    });
    return response.message;
  } catch (error) {
    throw error.response.data.detail;
  }
};

export const getDecks = () => api.get("/deck/list");

export const getGames = () => api.get("/game/list");

export const getGame = async (gameId) => {
  try {
    const response = await api.get("/game/get?game_id=" + gameId);
    return response.data.payload;
  } catch (error) {
    throw error.response.data.detail;
  }
};

export const playGame = async (gameId) => {
  try {
    const response = await api.post("/game/play", { id: gameId });
    return response.data.payload;
  } catch (error) {
    throw error.response.data.detail;
  }
};

export const createGame = async (gameName, decks, players, rounds) => {
  try {
    const response = await api.post("/game/start", {
      name: gameName,
      deck_names: decks,
      players: players,
      total_rounds: rounds,
    });
    return response.data.message;
  } catch (error) {
    throw error.response.data.detail;
  }
};

export const getCard = async (cardId) => {
  try {
    const response = await api.get("/card/get?card_id=" + cardId);
    return response.data.payload;
  } catch (error) {
    throw error.response.data.detail;
  }
};

export const updateCard = async (cardId, challenge) => {
  try {
    const response = await api.put("/card/edit", {
      id: cardId,
      challenge: challenge,
    });
    return response.data;
  } catch (error) {
    console.log(error);
    throw error.response.data.detail;
  }
};

export const createCard = async (deckId, challenge) => {
  try {
    const response = await api.post("/card/create", {
      deck_id: deckId,
      challenge: challenge,
    });
    return response.data;
  } catch (error) {
    console.log(error);
    throw error.response.data.detail;
  }
};

export const createDeck = async (deckName) => {
  try {
    const response = await api.post("/deck/create", { name: deckName });
    return response.data;
  } catch (error) {
    throw error.response.data.detail;
  }
};

export const getDeck = async (deckId) => {
  try {
    const response = await api.get("/deck/get?deck_id=" + deckId);
    return response.data.payload;
  } catch (error) {
    console.log(error);
    throw error.response.data.detail;
  }
};

export const updateDeck = async (deckId, deckNewName, settings) => {
  try {
    const response = await api.put("/deck/edit", {
      "id": deckId,
      "new_name": deckNewName,
      "settings": settings,
    });
    return response.data;
  } catch (error) {
    throw error.response.data.detail;
  }
};
