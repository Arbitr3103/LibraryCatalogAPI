from decouple import config
from sqlalchemy.orm import Session
from app.models import User
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30)


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


# Генерация токена доступа
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Проверка токена
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # здесь можно, например, извлечь 'sub' или другие данные
    except JWTError as e:
        return {"error": str(e)}  # Возвращаем ошибку или пустое значение
