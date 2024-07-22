from fastapi import APIRouter, Depends, HTTPException
from models import Game, User
from utils.authentication import jwt_required
from utils.exceptions import GameFinished
from utils.schemas import GameNameSchema, GameStartSchema, UserSchema

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
            detail=e,
        )
    return {"message": f"{game} created"}


@router.post("/play")
async def play_game(
    game_info: GameNameSchema, user_info: UserSchema = Depends(jwt_required)
):
    user = await User.get(username=user_info.username)
    if (game := await Game.get_or_none(name=game_info.name, creator=user)) is None:
        raise HTTPException(
            status_code=404, detail=f"Game with {game_info.name} does not exists"
        )
    if game.finished:
        raise HTTPException(
            status_code=404, detail=f"Game with {game_info.name} already ended"
        )
    try:
        challange, player = await game.get_next_turn()
        return {"message": "Sucessfully played", "challange": challange, "player": player}
    except GameFinished:
        await game.finish()
        return {"message": "Game finished"}


@router.get("/list")
async def list_user_games(user: UserSchema = Depends(jwt_required)):
    user = await User.get(username=user.username)
    games = (
        await Game.filter(creator=user, finished=False)
        .prefetch_related("decks")
        .all()
    )
    states = [await game.state for game in games]
    games_list = [
        {
            "id": game.id,
            "name": game.name,
            "decks": [{"id": deck.id, "name": deck.name} for deck in game.decks],
            "is_finished": game.finished,
            "challanges": state.challanges,
            "current_round": state.current_round,
            "total_rounds": state.total_rounds,
        }
        for game, state in zip(games, states)
    ]
    return {"payload": games_list, "message": "All games listed"}


@router.post("/end")
async def end_game(game_info: GameNameSchema, user: UserSchema = Depends(jwt_required)):
    game = await Game.get_or_none(name=game_info.name, creator=user)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f"Game with {game_info.name} not found"
        )
    if await game.is_finished:
        raise HTTPException(
            status_code=404, detail=f"Game with {game_info.name} already ended"
        )
    await game.finish()
    return {"message": f"{game} ended"}
