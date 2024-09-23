#!/usr/bin/env python3
"""declare User model
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base


Base = declarative_base()
engine = create_engine('sqlite:///:memeory:', echo=True)


class User(Base):
    """User mapping object and table declaration
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
