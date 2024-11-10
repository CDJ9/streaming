from sqlalchemy import Column, Integer, String  # Adjust imports as needed
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # Define Base here

# Example in SQLAlchemy Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


# Add other models here, using `Base` defined in this file
