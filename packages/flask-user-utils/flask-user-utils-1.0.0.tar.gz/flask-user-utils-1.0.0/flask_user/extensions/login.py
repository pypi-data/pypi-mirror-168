from flask import Flask
from flask_login import LoginManager
from flask_user.domain import User
from flask_user.repositories import UserRepository

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id) -> User:
    return UserRepository().get_by_id(user_id)


def init_app(app: Flask) -> None:
    login_manager.init_app(app)
