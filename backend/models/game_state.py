import random
from typing import List

from models import Card
from tortoise import fields
from tortoise.models import Model
from utils.exceptions import GameFinished


class GameState(Model):
    id = fields.IntField(pk=True)
    cards = fields.JSONField()
    current_index = fields.IntField()
    players = fields.JSONField()
    current_turn = fields.IntField()
    total_rounds = fields.IntField()

    @classmethod
    async def create(
        cls,
        cards: List[Card],
        players: List[str],
        total_rounds: int = 1,
        current_index: int = 0,
        current_turn: int = 0,
    ) -> "GameState":
        assert len(cards) > 0, "At least one card is required"
        assert len(players) > 0, "At least one player is required"
        assert len(cards) >= len(
            players
        ), "There must be at least as many cards as players"
        assert total_rounds > 0, "At least one round is required"
        total_rounds = min(
            total_rounds, _count_cards_for_all_players(cards) // len(players)
        )
        cards = await _generate_cards(cards, total_rounds)
        return await super().create(
            cards=cards,
            current_index=current_index,
            players=players,
            total_rounds=total_rounds,
            current_turn=current_turn,
        )

    @property
    def n_players(self) -> int:
        return len(self.players)

    @property
    def current_round(self) -> int:
        return self.current_turn // self.n_players

    @property
    def is_finished(self) -> bool:
        return (
            self.current_index >= len(self.cards)
            or self.current_round >= self.total_rounds
        )

    @property
    def current_card(self) -> str:
        return self.cards[self.current_index]

    @property
    def current_is_for_all_players(self) -> bool:
        return self.current_card["is_for_all_players"]

    @property
    def current_challenge(self) -> str:
        return self.current_card["challenge"]

    @property
    def current_is_hidden(self) -> bool:
        return self.current_card["is_hidden"]

    @property
    def current_player(self) -> str:
        if self.current_is_for_all_players:
            return "All"
        return self.players[self.current_turn % self.n_players]
    
    @property
    def challanges(self) -> List[str]:
        return [card["challenge"] for card in self.cards]

    async def next_turn(self) -> tuple[str, str]:
        if self.is_finished:
            raise GameFinished
        self.current_index += 1
        if not self.current_is_for_all_players:
            self.current_turn += 1
        if self.current_turn % self.n_players == 0:
            random.shuffle(self.players)
        await self.save()
        return self.current_challenge, self.current_player, self.current_is_hidden


async def _generate_cards(cards: list[Card], total_rounds: int) -> List[Card]:
    random.shuffle(cards)
    return [
        {
            "challenge": card.challenge,
            "is_for_all_players": await card.is_for_all_players,
            "is_hidden": await card.is_hidden,
        }
        for card in cards
    ]


def _count_cards_for_all_players(cards: list[Card]) -> int:
    return sum(1 for card in cards if card.is_for_all_players)
