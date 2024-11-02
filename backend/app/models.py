# app/models.py

"""
This file contains the SQLAlchemy models for Users and Rooms.

- The User model stores user information.
- The Room model stores video conferencing room information.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Define the base class for SQLAlchemy models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True)

    # Relationship: One user can have many rooms
    rooms = relationship("Room", back_populates="host")


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String, unique=True)
    host_id = Column(Integer, ForeignKey('users.id'))

    # Relationship: One room has one host (a User)
    host = relationship("User", back_populates="rooms")
