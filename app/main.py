from fastapi import FastAPI
import logging

from app.database import create_db
from app.auth import auth_router
from app.library import library_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="Library Catalog API")

# Создаем таблицы при запуске приложения
create_db()

# Подключаем роутеры
app.include_router(auth_router)
app.include_router(library_router)


@app.get("/")
def read_root():
    return {"message": "Library Catalog API is up and running"}
