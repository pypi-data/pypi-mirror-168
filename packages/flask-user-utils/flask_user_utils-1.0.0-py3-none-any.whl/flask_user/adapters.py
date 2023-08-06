from .repositories import UserRepository
from .domain import ILoginValidator, IRegistrationValidator


class LoginValidator(ILoginValidator):
    repository = UserRepository()


class RegistrationValidator(IRegistrationValidator):
    repository = UserRepository()
