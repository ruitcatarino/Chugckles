import os


class Settings:
    def __init__(self):
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")
        self.db_host = os.getenv("DB_HOST", "db")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.jwt_secret_key = os.getenv(
            "JWT_SECRET_KEY",
            "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
        )
        self.jwt_validity = int(os.getenv("JWT_VALIDITY", 7200))
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    def __getattr__(self, name):
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )


settings = Settings()
