from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# 1. Создаем асинхронный движок
# echo=True будет выводить SQL-запросы в консоль (полезно для отладки)
engine = create_async_engine(settings.DATABASE_URL_async, echo=True)

# 2. Создаем фабрику сессий
# expire_on_commit=False полезно для асинхронной работы
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# 3. Зависимость (dependency) для получения сессии в эндпоинтах
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session