from tortoise.models import Model
from tortoise import fields


class Card(Model):
    id = fields.IntField(pk=True)
    challenge = fields.TextField()
    deck = fields.ForeignKeyField("models.Deck", related_name="cards")

    class Meta:
        table = "cards"
        unique_together = [("challenge", "deck")]

    def __str__(self) -> str:
        return f"Card#{self.id}: {self.challenge}"

    def __repr__(self) -> str:
        return str(self)
    
    @property
    async def is_hidden(self) -> bool:
        deck = await self.deck
        return deck.is_hidden
    
    @property
    async def is_for_all_players(self) -> bool:
        deck = await self.deck
        return deck.is_for_all_players
