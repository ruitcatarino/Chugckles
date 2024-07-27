import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

export const login = async (username, password) => {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);
  try {
    const response = await axios.post(`${API_URL}/user/login`, formData.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data.token;
  } catch (error) {
    throw(error.response.data.detail);
  }
};

export const register = async (username, password) =>{
  try {
    const response = await api.post('/user/register', {
      username,
      password,
    });
    return response.message;
  } catch (error) {
    throw(error.response.data.detail);
  }
};

export const getDecks = () => api.get('/deck/list');

export const getDeckCards = (deckId) => api.get(`/card/list?deck_id=${deckId}`);

export const createCard = (deckId, cardData) =>
  api.post('/card/create', { deck_id: deckId, ...cardData });

export const editCard = (cardId, cardData) =>
  api.put(`/card/edit/${cardId}`, cardData);

export const createGame = (deckIds) =>
  api.post('/game/start', { deck_ids: deckIds });

export const getGames = () => api.get('/game/list');

export const playTurn = (gameId) => api.post(`/game/play/${gameId}`);

export const endGame = (gameId) => api.post(`/game/end/${gameId}`);

export const logout = () => {
  localStorage.removeItem('token');
};