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
        are_all_cards_for_all_players = await all_cards_are_for_all_players(cards)
        if not are_all_cards_for_all_players:
            total_turns = total_rounds * len(players)
        else:
            total_turns = total_rounds
        cards = await generate_cards(cards, total_turns, are_all_cards_for_all_players)
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
        return (self.current_turn // self.n_players) + 1

    @property
    def is_finished(self) -> bool:
        return self.current_index >= len(self.cards) - 1

    @property
    def current_card(self) -> dict:
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
    def challenges(self) -> List[str]:
        return [card["challenge"] for card in self.cards]

    @property
    def all_cards_are_for_all_players(self) -> bool:
        return all(card["is_for_all_players"] for card in self.cards)

    async def next_turn(self) -> tuple[str, str, bool]:
        if self.is_finished:
            raise GameFinished
        self.current_index += 1
        if not self.current_is_for_all_players:
            self.current_turn += 1
            if self.current_turn % self.n_players == 0:
                random.shuffle(self.players)
        if self.all_cards_are_for_all_players:
            self.current_turn += self.n_players
        await self.save()
        return self.current_challenge, self.current_player, self.current_is_hidden


async def generate_cards(
    cards: List[Card], total_turns: int, count_all_players_cards: bool = False
) -> List[dict]:
    random.shuffle(cards)
    data = []
    cards_in_data = 0
    for card in cards:
        data.append(
            {
                "challenge": card.challenge,
                "is_for_all_players": await card.is_for_all_players,
                "is_hidden": await card.is_hidden,
            }
        )
        if not await card.is_for_all_players or count_all_players_cards:
            cards_in_data += 1
        if cards_in_data == total_turns:
            return data
    raise AssertionError("Not enough cards")


async def count_cards_for_specific_players(cards: List[Card]) -> int:
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


async def all_cards_are_for_all_players(cards: List[Card]) -> bool:
    for card in cards:
        if not await card.is_for_all_players:
            return False
    return True
