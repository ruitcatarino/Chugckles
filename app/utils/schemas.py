from tortoise.contrib.pydantic import pydantic_model_creator
from models import Card, User
from pydantic import BaseModel


class CardCreationSchema(BaseModel):
    challenge: str
    deck_name: str


CardSchema = pydantic_model_creator(Card, name="Card", exclude=("id", "deck"))
UserSchema = pydantic_model_creator(User, name="User", exclude=("id", "disabled"))
