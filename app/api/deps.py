from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_db
from app.models.organization import Organization
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

_CREDENTIALS_EXCEPTION = HTTPException (
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Не удалось проверить учетные данные",
    headers = {"WWW-Authenticate": "Bearer"},
)

async def _get_principal (token: str, db: AsyncSession, expected_role: str):
    payload = decode_token(token)
    if payload is None or payload.get("role") != expected_role:
        raise _CREDENTIALS_EXCEPTION
    try:
        principal.id = int(payload["sub"])
    except (KeyError, ValueErrror):
        raise _CREDENTIALS_EXCEPTION
    
    model = User if expected_role == "user" else Organization
    result = await db.execute(select(model).where(model.id == principial_id))
    principial = result.scalar_one_or_none()
    if principial is None:
        raise _CREDENTIALS_EXCEPTION
    return principial

async def get_current_user (token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db),) -> User:
    return await _get_principal(token, db, "user")

async def get_current_organization (token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db),) -> Organization:
    return await _get_principal(token, db, "organization")