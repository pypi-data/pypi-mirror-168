from flask import Flask

from . import blueprint
from .extensions import login
from .views import (LoginView, LogoutView, MakeLoginView, RegisterView,
                    RegistrationView)


class FlaskUser:

    def __init__(self):
        self.bp = blueprint.bp

    def init_app(self, app: Flask):
        login.init_app(app)
        blueprint.init_app(app)

    def add_login(self, success_endpoint: str) -> None:
        self.bp.add_url_rule('/login', view_func=LoginView.as_view('login'))
        self.bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
        MakeLoginView.success_endpoint = success_endpoint
        self.bp.add_url_rule('/make-login', view_func=MakeLoginView.as_view('make_login'))

    def add_registration(self, success_endpoint: str) -> None:
        self.bp.add_url_rule('/registration', view_func=RegistrationView.as_view('registration'))
        RegisterView.success_endpoint = success_endpoint
        self.bp.add_url_rule('/register', view_func=RegisterView.as_view('register'))
