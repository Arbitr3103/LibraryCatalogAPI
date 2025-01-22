from decouple import config
from sqlalchemy.orm import Session
from app.models import User

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
