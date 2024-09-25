"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from typing import TypeVar

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """add a user
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> TypeVar('User'):
        """find user
        """
        for key in kwargs:
            if key not in User.__dict__.keys():
                raise InvalidRequestError

        if self._session.query(User).filter_by(**kwargs).first():
            return self._session.query(User).filter_by(**kwargs).first()
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """update user
        Args:
            user_id (int): User id to update object
        Returns:
            None
        """
        User_for_update = self.find_user_by(id=f'{user_id}')
        for key, value in kwargs.items():
            if key not in User_for_update.__dict__.keys():
                raise ValueError
            User_for_update.__dict__[key] = value
        self._session.commit()
        return
