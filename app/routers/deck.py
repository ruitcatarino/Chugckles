from fastapi import APIRouter, Depends, HTTPException
from models import Deck, Card
from utils.schemas import DeckSchema, DeckEditSchema, UserSchema
from utils.token import jwt_required

router = APIRouter(
    prefix="/deck",
    tags=["Deck"],
)


@router.post("/create")
async def create_deck(deck_body: DeckSchema, _: UserSchema = Depends(jwt_required)):
    if await Deck.exists(name=deck_body.name):
        raise HTTPException(
            status_code=404, detail=f"Deck with {deck_body.name} already exists"
        )
    deck = await Deck.create(name=deck_body.name)
    return {"message": f"{deck} created"}


@router.get("/list")
async def list_all_decks(_: UserSchema = Depends(jwt_required)):
    decks = await Deck.all().prefetch_related("cards")
    decks_list = [
        {
            "id": deck.id,
            "name": deck.name,
            "cards": [
                {"id": card.id, "challenge": card.challenge} for card in deck.cards
            ],
        }
        for deck in decks
    ]
    return {"payload": decks_list, "message": "All decks listed"}


@router.put("/edit")
async def edit_card(deck_body: DeckEditSchema, _: UserSchema = Depends(jwt_required)):
    deck = await Deck.get_or_none(name=deck_body.name)
    if deck is None:
        raise HTTPException(status_code=404, detail="Card not found")
    deck.name = deck_body.new_name
    await deck.save()
    return {"message": f"{deck} edited"}


@router.delete("/delete")
async def delete_deck(deck_body: DeckSchema, _: UserSchema = Depends(jwt_required)):
    deck = await Deck.get_or_none(name=deck_body.name)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    await deck.delete()
    return {"message": f"{deck} deleted"}
