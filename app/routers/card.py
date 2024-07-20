from fastapi import APIRouter, Depends, HTTPException
from models import Card, Deck
from utils.token import jwt_required
from utils.schemas import CardCreationSchema, UserSchema

router = APIRouter(
    prefix="/card",
    tags=["card"],
)


@router.post("/create")
async def create_card(
    card_body: CardCreationSchema, _: UserSchema = Depends(jwt_required)
):
    deck = await Deck.get_or_none(name=card_body.deck_name)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    card = await Card.create(challenge=card_body.challenge, deck=deck)
    return {"message": card}
