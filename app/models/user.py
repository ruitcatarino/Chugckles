from tortoise.models import Model
from tortoise import fields
import hashlib


class User(Model):
    username = fields.TextField()
    password = fields.TextField()

    @classmethod
    async def create(cls, username: str, password: str):
        hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        return await super().create(username=username, password=hashed_password)

    async def check_password(self, password: str):
        return hashlib.sha512(password) == password

    def __str__(self):
        return f"{self.username} - {self.password}"
