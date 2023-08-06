from .domain import IUserRepository, User, UserData
from .models import UserModel
from .database import session


class UserRepository(IUserRepository):

    def create(self, user_data: UserData) -> User:
        session.add(
            UserModel(email=user_data.email, password=user_data.password))
        session.commit()
        return self.get_by_email(user_data.email)

    def get_by_email(self, email: str) -> User | None:
        user = session.query(UserModel).filter_by(email=email).first()
        if user:
            return self.to_dataclass(user)

    def get_by_id(self, id: int) -> User | None:
        user = session.query(UserModel).get(id)
        if user:
            return self.to_dataclass(user)

    def to_dataclass(self, model: UserModel) -> User:
        return User(id=model.id,
                    email=model.email,
                    password=model.password,
                    is_superuser=model.is_superuser)
