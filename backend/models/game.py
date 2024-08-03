from typing import List
import random

from models.deck import Deck
from models.card import Card
from models.user import User
from tortoise import fields
from tortoise.models import Model
from utils.exceptions import GameFinished


class Game(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    creator = fields.ForeignKeyField("models.User", related_name="games")
    decks = fields.ManyToManyField("models.Deck", related_name="games")
    cards = fields.ManyToManyField("models.Card", related_name="in_games")
    current_card = fields.ForeignKeyField(
        "models.Card", related_name="currently_in_games", null=True
    )
    players = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)
    finished = fields.BooleanField(default=False)
    current_turn = fields.IntField()
    total_turns = fields.IntField()
    total_rounds = fields.IntField()

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
        assert len(players) > 0, "At least one player is required"
        players.append(creator.username)

        decks = await Deck.filter(name__in=deck_names).prefetch_related("cards")
        missing_decks = set(deck_names) - {deck.name for deck in decks}
        assert not missing_decks, f"Decks {missing_decks} not found"

        cards = [card for deck in decks for card in deck.cards]
        assert len(cards) > 0, "At least one card is required"

        assert total_rounds > 0, "At least one round is required"

        if await all_cards_are_for_all_players(cards):
            total_turns = total_rounds
        else:
            total_turns = total_rounds * len(players)

        if await all_cards_are_for_all_players(cards):
            assert total_turns < await count_cards_for_all_players(
                cards
            ), "Not enough cards"
        else:
            assert total_turns < await count_cards_not_for_all_players(
                cards
            ), "Not enough cards"

        game = await super().create(
            name=name,
            creator=creator,
            players=players,
            current_turn=0,
            total_turns=total_turns,
            total_rounds=total_rounds,
        )
        await game.decks.add(*decks)
        await game.cards.add(*cards)
        await game.draw_card()
        return game

    def __str__(self) -> str:
        return self.name

    @property
    def n_players(self) -> int:
        return len(self.players)

    @property
    async def current_round(self) -> int:
        if not await self.all_cards_are_for_all_players:
            return (self.current_turn // self.n_players) + 1
        else:
            return self.current_turn + 1

    @property
    async def is_finished(self) -> bool:
        return self.current_turn >= self.total_turns - 1

    @property
    async def current_is_for_all_players(self) -> bool:
        current_card = await self.current_card
        return await current_card.is_for_all_players

    @property
    async def current_challenge(self) -> str:
        current_card = await self.current_card
        return current_card.challenge

    @property
    async def current_is_hidden(self) -> bool:
        current_card = await self.current_card
        return await current_card.is_hidden

    @property
    async def current_deck(self) -> str:
        current_card = await self.current_card
        return await current_card.deck

    @property
    async def current_player(self) -> str:
        if await self.current_is_for_all_players:
            return "All"
        return self.players[self.current_turn % self.n_players]

    @property
    async def challenges(self) -> List[str]:
        cards = await self.cards
        return [card.challenge for card in cards]

    @property
    async def all_cards_are_for_all_players(self) -> bool:
        cards = await self.cards
        for card in cards:
            if not await card.is_for_all_players:
                return False
        return True

    async def finish(self) -> None:
        self.finished = True
        await self.save()

    async def draw_card(self) -> dict:
        cards = await self.cards
        card = random.choice(cards)
        await self.cards.remove(card)
        self.current_card = card
        await self.save()
        return card

    async def increment_turn(self) -> None:
        if await self.is_finished:
            raise GameFinished
        if (
            not await self.current_is_for_all_players
            or await self.all_cards_are_for_all_players
        ):
            self.current_turn += 1

        await self.draw_card()
        await self.save()

        if await self.is_finished:
            await self.finish()


async def all_cards_are_for_all_players(cards: List[Card]) -> bool:
    for card in cards:
        if not await card.is_for_all_players:
            return False
    return True


async def count_cards_not_for_all_players(cards: List[Card]) -> int:
    count = 0
    for card in cards:
        if not await card.is_for_all_players:
            count += 1
    return count


async def count_cards_for_all_players(cards: List[Card]) -> int:
    count = 0
    for card in cards:
        if await card.is_for_all_players:
            count += 1
    return count
