from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from decouple import config

from app.models import User
from app.schemas import UserCreate, Token
from app.database import get_db

# Хэширование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Для работы с токенами
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Инициализация роутера
auth_router = APIRouter(prefix="/auth", tags=["Auth"])


# Переносим SECRET_KEY в функцию
def get_secret_key() -> str:
    """Функция для получения SECRET_KEY из переменных окружения."""
    return config("SECRET_KEY", default="fallback_default_key")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хэширует пароль."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создает access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_secret_key(), algorithm="HS256")


def get_user(db: Session, username: str) -> Optional[User]:
    """Получает пользователя из базы данных по имени."""
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> User:
    """Аутентифицирует пользователя."""
    user = get_user(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def register_user(db: Session, user: UserCreate) -> User:
    """Регистрирует пользователя."""
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@auth_router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Эндпоинт для регистрации пользователя."""
    existing_user = get_user(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже зарегистрирован",
        )
    db_user = register_user(db, user)
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Эндпоинт для аутентификации пользователя."""
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/me", response_model=UserCreate)
def read_users_me(current_user: User = Depends(oauth2_scheme)):
    """Эндпоинт для получения данных текущего пользователя."""
    return current_user
