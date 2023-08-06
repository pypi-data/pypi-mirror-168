import re
from re import Pattern
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass

from .utils import IValidator


@dataclass
class User:
    id: int
    email: str
    password: str
    is_superuser: bool = False
    is_active: bool = True
    is_authenticated: bool = is_active
    is_anonymous: bool = False

    def get_id(self):
        return str(self.id)


@dataclass
class UserData:
    email: str
    password: str


class IUserRepository(ABC):

    @abstractmethod
    def create(self, user_data: UserData) -> User:
        raise NotImplementedError()

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, id: int) -> User | None:
        raise NotImplementedError()


@dataclass
class EmailValidator(IValidator):
    value: str

    @property
    def email_regex(self) -> Pattern:
        return re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    def is_valid(self) -> bool:
        if self.email_regex.findall(self.value):
            return super().is_valid()
        return False


class IUserAction(ABC):

    @abstractproperty
    def repository(self) -> IUserRepository:
        raise NotImplementedError()


@dataclass
class ILoginValidator(IValidator, IUserAction):
    user_data: UserData
    superuser_login: bool = False

    def is_valid(self):
        self.set_next(EmailValidator(self.user_data.email))
        try:
            user = self.repository.get_by_email(self.user_data.email)
            assert user and user.password == self.user_data.password
            assert user.is_superuser or not self.superuser_login
            return super().is_valid()
        except AssertionError:
            return False


@dataclass
class IRegistrationValidator(IValidator, IUserAction):
    user_data: UserData

    def is_valid(self) -> bool:
        self.set_next(EmailValidator(self.user_data.email))
        user = self.repository.get_by_email(self.user_data.email)
        return False if user else super().is_valid()
