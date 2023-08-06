from abc import ABC, abstractmethod, abstractproperty

from flask import Response, redirect, render_template, request, url_for
from flask.views import MethodView
from flask_login import login_user, logout_user

from .adapters import LoginValidator, RegistrationValidator
from .domain import UserData
from .forms import UserForm
from .repositories import UserRepository
from .utils import IValidator


class IUserActionView(ABC, MethodView):

    @abstractproperty
    def validator(self) -> IValidator:
        raise NotImplementedError()

    @abstractproperty
    def error_message(self) -> str:
        raise NotImplementedError()

    @abstractproperty
    def failure_endpoint(self) -> str:
        raise NotImplementedError()

    def post(self) -> Response:
        user_data = UserData(request.form['email'], request.form['password'])
        if self.validator(user_data).is_valid():
            self.make_action(user_data)
            return redirect(url_for(self.success_endpoint))
        return redirect(url_for(self.failure_endpoint, error_message=self.error_message))

    @abstractmethod
    def make_action(self, user_data: UserData) -> None:
        raise NotImplementedError()


class LoginView(MethodView):

    def get(self) -> Response:
        return render_template('user/login.html', form=UserForm(),
                               form_action=url_for('.make_login'))


class MakeLoginView(IUserActionView):
    validator = LoginValidator
    error_message = 'Email ou senha invalidos'
    superuser_login = False
    failure_endpoint = '.login'

    def post(self) -> Response:
        self.validator.superuser_login = self.superuser_login
        return super().post()

    def make_action(self, user_data: UserData) -> None:
        login_user(UserRepository().get_by_email(user_data.email))


class LogoutView(MethodView):

    def get(self):
        logout_user()
        return redirect(url_for('.login'))


class RegistrationView(MethodView):

    def get(self) -> Response:
        return render_template('user/registration.html', form=UserForm(),
                               form_action=url_for('.register'))


class RegisterView(IUserActionView):
    validator = RegistrationValidator
    error_message = 'Email já cadastrado'
    failure_endpoint = '.registration'

    def make_action(self, user_data: UserData) -> None:
        UserRepository().create(user_data)
