from typing import List

from models.deck import Deck
from models.game_state import GameState
from models.user import User
from tortoise import fields
from tortoise.models import Model
from utils.exceptions import GameFinished


class Game(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    creator = fields.ForeignKeyField("models.User", related_name="games")
    decks = fields.ManyToManyField("models.Deck", related_name="decks")
    cards = fields.ManyToManyField("models.Card", related_name="cards")
    state = fields.OneToOneField("models.GameState", related_name="game")
    players = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)
    finished = fields.BooleanField(default=False)

    class Meta:
        table = "games"

    @classmethod
    async def create(
        cls,
        name: str,
        players: List[str],
        creator: User,
        deck_names: List[str],
        total_rounds: int,
    ) -> "Game":
        players.append(creator.username)
        try:
            decks = await Deck.filter(name__in=deck_names).prefetch_related("cards")
            missing_decks = set(deck_names) - {deck.name for deck in decks}
            assert not missing_decks, f"Decks {missing_decks} not found"
            cards = [card for deck in decks for card in deck.cards]
            state = await GameState.create(
                cards=cards, players=players, total_rounds=total_rounds
            )
        except AssertionError as e:
            raise e
        game = await super().create(
            name=name,
            creator=creator,
            players=players,
            state=state,
        )
        await game.decks.add(*decks)
        await game.cards.add(*cards)
        return game

    def __str__(self) -> str:
        return self.name

    async def finish(self) -> None:
        self.finished = True
        await self.save()

    async def get_next_turn(self) -> tuple[str, str]:
        if self.finished:
            raise GameFinished

        try:
            state = await self.state
            data = await state.next_turn()
            if state.is_finished:
                await self.finish()
            return data
        except GameFinished:
            await self.finish()
            raise GameFinished
