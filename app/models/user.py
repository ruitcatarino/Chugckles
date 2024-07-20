import hashlib

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=130)
    disabled = fields.BooleanField()

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


UserPydantic = pydantic_model_creator(User, name="User", exclude=("id", "disabled"))
