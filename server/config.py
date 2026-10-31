from dotenv import load_dotenv

load_dotenv()


import os

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "development-secret-key-change-this"
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///productivity.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    JWT_SECRET_KEY = os.environ.get(
        "JWT_SECRET_KEY",
        "development-jwt-secret-change-tis"
    )

    JWT_ACCESS_TOKEN_EXPIRES = 3600
