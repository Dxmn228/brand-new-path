import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context

# 1. Добавляем корень проекта в пути поиска Python
sys.path.append(str(Path(__file__).resolve().parents[1]))

# 2. Импортируем настройки (из .env) и модели
from app.core.config import settings
from app.db.base import Base
import app.models  # Этот импорт ОБЯЗАТЕЛЕН, чтобы Alembic увидел твои таблицы

# 3. Получаем объект конфигурации Alembic
config = context.config

# 4. Настраиваем логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 5. Передаем Alembic'у адрес базы данных из твоего .env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_sync)

# 6. Указываем, где лежат метаданные (описания таблиц)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Режим без подключения к БД (только генерация SQL)"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Режим с реальным подключением к БД"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()