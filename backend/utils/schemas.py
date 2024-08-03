from tortoise.contrib.pydantic import pydantic_model_creator
from models import Card, User, Deck, Game
from pydantic import BaseModel
from typing import List, Optional

CardSchema = pydantic_model_creator(Card, name="Card", exclude=("id", "deck"))
DeckSchema = pydantic_model_creator(
    Deck, name="Deck", exclude=("id", "cards", "settings")
)
UserSchema = pydantic_model_creator(User, name="User", exclude=("id", "disabled"))
GameSchema = pydantic_model_creator(
    Game, name="Game", exclude=("id", "creator", "state", "created_at", "finished")
)


class CardCreationSchema(BaseModel):
    challenge: str
    deck_id: int


class CardEditSchema(BaseModel):
    id: int
    challenge: str


class CardIdSchema(BaseModel):
    id: int


class DeckCreateSchema(BaseModel):
    name: str
    settings: Optional[dict] = {}


class DeckEditSchema(BaseModel):
    id: int
    new_name: Optional[str] = ""
    settings: Optional[dict] = {}


class DeckNameSchema(BaseModel):
    name: str


class GameStartSchema(BaseModel):
    name: str
    deck_names: List[str]
    players: List[str]
    total_rounds: int


class GameIdSchema(BaseModel):
    id: int
