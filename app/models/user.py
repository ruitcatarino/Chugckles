import hashlib

from tortoise import fields
from tortoise.models import Model
from models.game import Game


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=130)
    disabled = fields.BooleanField()
    games: fields.ReverseRelation["Game"]

    class Meta:
        table = "users"

    @classmethod
    async def create(cls, username: str, password: str, disabled: bool = False):
        return await super().create(
            username=username,
            password=await cls._hash_password(password),
            disabled=disabled,
        )

    async def check_password(self, password: str):
        return await self._hash_password(password) == self.password

    @staticmethod
    async def _hash_password(password: str):
        return hashlib.sha512(password.encode("utf-8")).hexdigest()

    def __str__(self):
        return f"{self.username}"
