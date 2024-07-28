from fastapi import APIRouter, Depends, HTTPException
from models import Card, Deck
from utils.authentication import jwt_required
from utils.schemas import CardCreationSchema, CardIdSchema, CardEditSchema, UserSchema

router = APIRouter(
    prefix="/card",
    tags=["Card"],
)


@router.post("/create")
async def create_card(
    card_body: CardCreationSchema, _: UserSchema = Depends(jwt_required)
):
    deck = await Deck.get_or_none(name=card_body.deck_name)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    if await Card.exists(challenge=card_body.challenge, deck=deck):
        raise HTTPException(
            status_code=404, detail="Card with these values already exists"
        )
    card = await Card.create(challenge=card_body.challenge, deck=deck)
    return {"message": f"{card} created"}


@router.get("/list")
async def list_all_cards(_: UserSchema = Depends(jwt_required)):
    cards = await Card.all().prefetch_related("deck")
    cards_list = [
        {
            "id": card.id,
            "deck_id": card.deck.id,
            "deck_name": card.deck.name,
            "challenge": card.challenge,
        }
        for card in cards
    ]
    return {"payload": cards_list, "message": "All cards listed"}


@router.get("/get")
async def get_card(card_id: CardIdSchema, UserSchema=Depends(jwt_required)):
    card = await Card.get_or_none(id=card_id.id).prefetch_related("deck")
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return {
        "payload": {
            "id": card.id,
            "deck_id": card.deck.id,
            "deck_name": card.deck.name,
            "challenge": card.challenge,
        },
        "message": "All cards listed",
    }


@router.put("/edit")
async def edit_card(card_body: CardEditSchema, _: UserSchema = Depends(jwt_required)):
    card = await Card.get_or_none(id=card_body.id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    card.challenge = card_body.challenge
    await card.save()
    return {"message": f"Card#{card.id} edited"}


@router.delete("/delete")
async def delete_card(card_id: CardIdSchema, _: UserSchema = Depends(jwt_required)):
    card = await Card.get_or_none(id=card_id.id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    await card.delete()
    return {"message": f"{card} deleted"}
