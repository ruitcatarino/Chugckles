from tortoise.models import Model
from tortoise import fields
from models.card import Card


class Deck(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20, unique=True)
    cards = fields.ReverseRelation["Card"]
    settings = fields.JSONField()

    class Meta:
        table = "decks"

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return str(self)

    @property
    def is_hidden(self) -> bool:
        return self.settings.get("hidden", False)

    @property
    def is_for_all_players(self) -> bool:
        return self.settings.get("for_all_players", False)

    async def get_settings(self) -> dict:
        return {
            "hidden": self.is_hidden,
            "for_all_players": self.is_for_all_players,
        }
