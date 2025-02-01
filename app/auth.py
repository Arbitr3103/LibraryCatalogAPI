from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.models import LibraryItem
import logging

from app.models import User
from app.schemas import UserCreate, Token, UserResponse, LibraryItemResponse
from app.database import get_db
from app.utils import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Хэширование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Для работы с токенами
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Инициализация роутера
auth_router = APIRouter(prefix="/auth", tags=["Auth"])
library_router = APIRouter(prefix="/library_items", tags=["Library Items"])
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# ============================
# Вспомогательные функции
# ============================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хэширует пароль."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создает access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user(db: Session, username: str) -> Optional[User]:
    """Получает пользователя из базы данных по имени."""
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> User:
    """Аутентифицирует пользователя."""
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def register_user(db: Session, user: UserCreate) -> User:
    """Регистрирует нового пользователя в базе данных."""
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    except Exception as e:
        logger.error(f"Ошибка при регистрации пользователя: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка регистрации пользователя. Попробуйте позже.")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Получает текущего пользователя на основе токена."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = get_user(db, username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ============================
# Эндпоинты
# ============================

@auth_router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Эндпоинт для регистрации нового пользователя."""
    logger.info("Получен запрос: %s", user.dict(exclude={"password"}))

    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        field = "имя" if existing_user.username == user.username else "email"
        logger.warning("Попытка регистрации с уже существующим %s: %s", field, user.dict()[field])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с таким {field} уже зарегистрирован.",
        )

    db_user = register_user(db, user)
    logger.info("Успешно создан пользователь: %s", db_user.username)

    access_token = create_access_token(data={"sub": db_user.username})
    logger.info("Создан токен для пользователя: %s", db_user.username)

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Эндпоинт для аутентификации пользователя."""
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Эндпоинт для получения данных текущего пользователя."""
    return current_user


@library_router.get("/", response_model=List[LibraryItemResponse])
def get_library_items(
        db: Session = Depends(get_db),
        author: Optional[str] = None,
        published_year: Optional[int] = None,
        genre: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
):
    """
    Получает список элементов библиотеки с фильтрацией по автору, году публикации и жанру.
    """
    query = db.query(LibraryItem)

    if author:
        query = query.filter(LibraryItem.author.ilike(f"%{author}%"))
    if published_year:
        query = query.filter(LibraryItem.published_year == published_year)
    if genre:
        query = query.filter(LibraryItem.genre.ilike(f"%{genre}%"))

    items = query.offset(skip).limit(limit).all()
    return items
