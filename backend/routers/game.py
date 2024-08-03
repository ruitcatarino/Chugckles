from fastapi import APIRouter, Depends, HTTPException
from models import Game, User
from utils.authentication import jwt_required
from utils.exceptions import GameFinished
from utils.schemas import GameIdSchema, GameStartSchema, UserSchema

router = APIRouter(
    prefix="/game",
    tags=["Game"],
)


@router.post("/start")
async def start_game(
    game_info: GameStartSchema, user_info: UserSchema = Depends(jwt_required)
):
    if await Game.exists(name=game_info.name):
        raise HTTPException(
            status_code=404, detail=f"Game with {game_info.name} already exists"
        )
    user = await User.get(username=user_info.username)
    try:
        game = await Game.create(
            name=game_info.name,
            players=game_info.players,
            creator=user,
            deck_names=game_info.deck_names,
            total_rounds=game_info.total_rounds,
        )
    except AssertionError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    return {"message": f"{game} created"}


@router.post("/play")
async def play_game(
    game_info: GameIdSchema, user_info: UserSchema = Depends(jwt_required)
):
    user = await User.get(username=user_info.username)
    game = await Game.get_or_none(id=game_info.id, creator=user)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f"Game with {game_info.id} does not exists"
        )
    if game.finished:
        {"message": "Game finished"}
    try:
        challenge, deck_name , player, is_hidden = await game.get_next_turn()
        return {
            "message": "Sucessfully played",
            "payload": {
                "challenge": challenge,
                "player": player,
                "is_hidden": is_hidden,
                "current_round": await game.current_round,
                "total_rounds": game.total_rounds,
                "deck_name": deck_name
            },
        }
    except GameFinished:
        await game.finish()
        return {"message": "Game finished"}


@router.get("/list")
async def list_user_games(user: UserSchema = Depends(jwt_required)):
    user = await User.get(username=user.username)
    games = (
        await Game.filter(creator=user, finished=False).prefetch_related("decks").all()
    )
    games_list = [
        {
            "id": game.id,
            "name": game.name,
            "decks": [{"id": deck.id, "name": deck.name} for deck in game.decks],
            "is_finished": game.finished,
            "challenges": await game.challenges,
            "current_round": await game.current_round,
            "total_rounds": game.total_rounds,
        }
        for game in games
    ]
    return {"payload": games_list, "message": "Unfinished games listed"}


@router.get("/list_all")
async def list_all_user_games(user: UserSchema = Depends(jwt_required)):
    user = await User.get(username=user.username)
    games = await Game.filter(creator=user).prefetch_related("decks").all()
    games_list = [
        {
            "id": game.id,
            "name": game.name,
            "decks": [{"id": deck.id, "name": deck.name} for deck in game.decks],
            "is_finished": await game.finished,
            "challenges": await game.challenges,
            "current_round": await game.current_round,
            "total_rounds": await game.total_rounds,
        }
        for game in games
    ]
    return {"payload": games_list, "message": "All games listed"}


@router.get("/get")
async def get_game(game_id: int, user: UserSchema = Depends(jwt_required)):
    user = await User.get(username=user.username)
    game = await Game.get_or_none(
        id=game_id, creator=user, finished=False
    ).prefetch_related("decks")
    if game is None:
        raise HTTPException(status_code=404, detail=f"Game with {game_id} not found")
    deck = await game.current_deck
    return {
        "payload": {
            "id": game.id,
            "name": game.name,
            "decks": [{"id": deck.id, "name": deck.name} for deck in game.decks],
            "is_finished": game.finished,
            "challenges": await game.challenges,
            "current_round": await game.current_round,
            "total_rounds": game.total_rounds,
            "current_turn": game.current_turn,
            "current_player": await game.current_player,
            "current_challenge": await game.current_challenge,
            "current_is_hidden": await game.current_is_hidden,
            "current_deck_name": deck.name,
        },
        "message": "Game found",
    }


@router.post("/end")
async def end_game(game_info: GameIdSchema, user: UserSchema = Depends(jwt_required)):
    game = await Game.get_or_none(id=game_info.id, creator=user)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f"Game with {game_info.id} not found"
        )
    if await game.is_finished:
        raise HTTPException(
            status_code=404, detail=f"Game with {game_info.id} already ended"
        )
    await game.finish()
    return {"message": f"{game} ended"}
