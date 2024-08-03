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
    decks = fields.ManyToManyField("models.Deck", related_name="decks")
    cards = fields.ManyToManyField("models.Card", related_name="cards")
    players = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)
    finished = fields.BooleanField(default=False)
    current_index = fields.IntField()
    current_turn = fields.IntField()
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
        assert len(cards) >= len(
            players
        ), "There must be at least as many cards as players"

        assert total_rounds > 0, "At least one round is required"

        are_all_cards_for_all_players = await all_cards_are_for_all_players(cards)
        if not are_all_cards_for_all_players:
            total_turns = total_rounds * len(players)
        else:
            total_turns = total_rounds

        cards = await generate_cards(cards, total_turns, are_all_cards_for_all_players)

        game = await super().create(
            name=name,
            creator=creator,
            players=players,
            current_index=0,
            current_turn=0,
            total_rounds=total_rounds,
        )
        await game.decks.add(*decks)
        await game.cards.add(*cards)
        return game

    def __str__(self) -> str:
        return self.name

    @property
    def n_players(self) -> int:
        return len(self.players)

    @property
    async def current_round(self) -> int:
        return (self.current_turn // self.n_players) + 1

    @property
    async def is_finished(self) -> bool:
        cards = await self.cards
        return self.current_index >= len(cards) - 1

    @property
    async def current_card(self) -> dict:
        cards = await self.cards
        return cards[self.current_index]

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

    async def get_next_turn(self) -> tuple[str, str]:
        if await self.is_finished:
            raise GameFinished
        self.current_index += 1
        if not await self.current_is_for_all_players:
            self.current_turn += 1
            if self.current_turn % self.n_players == 0:
                random.shuffle(self.players)
        if await self.all_cards_are_for_all_players:
            self.current_turn += self.n_players
        await self.save()
        deck = await self.current_deck
        return (
            await self.current_challenge,
            deck.name,
            await self.current_player,
            await self.current_is_hidden,
        )


async def generate_cards(
    cards: List[Card], total_turns: int, count_all_players_cards: bool = False
) -> List[Card]:
    random.shuffle(cards)
    data = []
    cards_in_data = 0
    for card in cards:
        data.append(card)
        if not await card.is_for_all_players or count_all_players_cards:
            cards_in_data += 1
        if cards_in_data == total_turns:
            return data
    raise AssertionError("Not enough cards")


async def all_cards_are_for_all_players(cards: List[Card]) -> bool:
    for card in cards:
        if not await card.is_for_all_players:
            return False
    return True
