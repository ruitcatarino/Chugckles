import random
from typing import List

from models import Card
from tortoise import fields
from tortoise.models import Model
from utils.exceptions import GameFinished


class GameState(Model):
    id = fields.IntField(pk=True)
    challanges = fields.JSONField()
    players = fields.JSONField()
    current_turn = fields.IntField()
    total_rounds = fields.IntField()

    @classmethod
    async def create(
        cls,
        cards: List[Card],
        players: List[str],
        total_rounds: int = 1,
        current_turn: int = 0,
    ) -> "GameState":
        assert len(cards) > 0, "At least one card is required"
        assert len(players) > 0, "At least one player is required"
        assert total_rounds > 0, "At least one round is required"
        random.shuffle(players)
        return await super().create(
            challanges=[card.challenge for card in _draw_cards(cards, total_rounds, len(players))],
            players=players,
            total_rounds=min(total_rounds, len(cards) // len(players)),
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
        return self.current_round >= self.total_rounds
    
    @property
    def current_player(self) -> str:
        return self.players[self.current_turn % self.n_players]
    
    @property
    def current_challenge(self) -> str:
        return self.challanges[self.current_turn]

    async def next_turn(self) -> tuple[str, str]:
        if self.is_finished: 
            raise GameFinished
        challange = self.challanges[self.current_turn]
        self.current_turn += 1
        await self.save()
        return challange, self.current_player

def _draw_cards(cards: list[Card], total_rounds: int, n_players: int) -> List[Card]:
    card_list = list(cards)
    cards_needed = min(total_rounds * n_players, len(card_list))
    random.shuffle(card_list)
    return card_list[:cards_needed]
