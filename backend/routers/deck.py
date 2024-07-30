from fastapi import APIRouter, Depends, HTTPException
from models import Deck
from utils.schemas import DeckSchema, DeckEditSchema, UserSchema, DeckCreateSchema
from utils.authentication import jwt_required

router = APIRouter(
    prefix="/deck",
    tags=["Deck"],
)


@router.post("/create")
async def create_deck(deck_body: DeckCreateSchema, _: UserSchema = Depends(jwt_required)):
    if await Deck.exists(name=deck_body.name):
        raise HTTPException(
            status_code=404, detail=f"Deck with {deck_body.name} already exists"
        )
    deck = await Deck.create(name=deck_body.name, settings=deck_body.settings)
    return {"message": f"{deck} created"}


@router.get("/list")
async def list_all_decks(_: UserSchema = Depends(jwt_required)):
    decks = await Deck.all().prefetch_related("cards")
    decks_list = [
        {
            "id": deck.id,
            "name": deck.name,
            "settings": await deck.get_settings(),
            "cards": [
                {"id": card.id, "challenge": card.challenge} for card in deck.cards
            ],
        }
        for deck in decks
    ]
    return {"payload": decks_list, "message": "All decks listed"}


@router.get("/get")
async def get_deck(deck_id: int, _: UserSchema = Depends(jwt_required)):
    deck = await Deck.get_or_none(id=deck_id).prefetch_related("cards")
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return {
        "payload": {
            "id": deck.id,
            "name": deck.name,
            "cards": [
                {"id": card.id, "challenge": card.challenge} for card in deck.cards
            ],
            "settings": await deck.get_settings(),
        },
        "message": "All decks listed",
    }


@router.put("/edit")
async def edit_card(deck_body: DeckEditSchema, _: UserSchema = Depends(jwt_required)):
    deck = await Deck.get_or_none(id=deck_body.id)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    if deck_body.new_name:
        deck.name = deck_body.new_name
    if deck_body.settings:
        deck.settings = deck_body.settings
    await deck.save()
    return {"message": f"{deck} edited"}



@router.delete("/delete")
async def delete_deck(deck_body: DeckSchema, _: UserSchema = Depends(jwt_required)):
    deck = await Deck.get_or_none(name=deck_body.name)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    await deck.delete()
    return {"message": f"{deck} deleted"}
