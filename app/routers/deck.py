from fastapi import APIRouter, Depends, HTTPException
from models import Deck
from utils.schemas import DeckSchema, UserSchema
from utils.token import jwt_required

router = APIRouter(
    prefix="/deck",
    tags=["Deck"],
)


@router.post("/create")
async def deck(
    deck_body: DeckSchema, _: UserSchema = Depends(jwt_required)
):
    if await Deck.exists(name=deck_body.name):
        raise HTTPException(status_code=404, detail="Deck name already exists")
    deck = await Deck.create(name=deck_body.name)
    return {"message": f"{deck} created"}
