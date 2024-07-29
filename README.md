# Chugckles

## Overview
This is a fullstack app designed to make a night of drinking more fun and full of exciting challenges, similar to the Picolo Party game, but as a free, open-source, and self-hostable alternative. The backend is built with FastAPI and the frontend with React JavaScript.

### Backend
The backend provides endpoints for user authentication, card and deck management, and game management.

You can populate the database with sample cards and decks using the `POPULATE_DATA` variable in the `backend/utils/__init__.py` file.

The API endpoints are as follows:
#### Authentication

    POST /user/register - Register a new user
    POST /user/login - Login a user

#### Card

    POST /card/create - Create a new card
    GET /card/list - List all cards
    GET /card/get - Get details of a specific card
    PUT /card/edit - Edit a card
    DELETE /card/delete - Delete a card

#### Deck

    POST /deck/create - Create a new deck
    GET /deck/list - List all decks
    GET /deck/get - Get details of a specific deck
    PUT /deck/edit - Edit a deck
    DELETE /deck/delete - Delete a deck

#### Game

    POST /game/start - Start a new game
    POST /game/play - Play a game
    GET /game/list - List user games
    GET /game/list_all - List all user games
    GET /game/get - Get details of a specific game
    POST /game/end - End a game

### Frontend
The frontend interacts with these endpoints to create a seamless user experience.

## Setup
To run the project, use Docker Compose:
1. Clone the repository:
```sh
git clone https://github.com/ruitcatarino/Chugckles.git
cd sipsync
```
2. Start the application:
```sh
docker compose up -d
```
The backend API will be available at http://127.0.0.1:8000 and the frontend application at http://localhost:3000.


## Contributing
Pull requests and helping hands in improvements are more than welcome! As a backend developer, I acknowledge that the frontend may not be perfect and would greatly appreciate any assistance in making it better.

## License
This project is open-source and available under the [MIT License](LICENSE.md). You are free to use, modify, and distribute it in accordance with the license terms.

## Disclaimer
This project is intended for entertainment purposes only. Excessive alcohol consumption can be harmful to health and may lead to dangerous situations. I do not endorse or encourage excessive drinking, and I strongly advise responsible behavior. Please enjoy this game responsibly, and ensure that all participants drink within their limits. Drink in moderation and never drink and drive. It's essential to prioritize your safety and well-being.
