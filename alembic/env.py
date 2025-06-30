from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Добавьте эти строки:
import os
import sys
from app.models import Base
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Это подключение к БД из docker-compose
config = context.config
config.set_main_option("sqlalchemy.url", "postgresql://postgres:postgres@db:5432/taskdb")

fileConfig(config.config_file_name)

target_metadata = Base.metadata  # Используем метаданные из моделей SQLAlchemy

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
