from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Загрузим переменные окружения из .env
from dotenv import load_dotenv

load_dotenv()

import os

# Получаем конфигурацию Alembic из alembic.ini
config = context.config

# Переопределяем sqlalchemy.url из переменной окружения DATABASE_URL,
# если она установлена.
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# Настройка логирования из файла ini
fileConfig(config.config_file_name)

# Импортируем Base из вашего приложения
from app.models import Base

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
