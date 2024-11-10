from sqlalchemy.orm import Session
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, username: str, password: str, email: str):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, password=hashed_password, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not pwd_context.verify(password, user.password):
        return None
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
