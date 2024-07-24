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
