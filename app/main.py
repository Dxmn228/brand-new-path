from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title="brand-new-path API",
    description="API для бронирования экскурсий",
    version="0.2.0",
)

# Настройка CORS (чтобы фронтенд мог делать запросы)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем все наши эндпоинты
app.include_router(api_router)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}