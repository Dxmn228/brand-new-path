from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token, generate_refresh_token, hash_password,
    hash_refresh_token, verify_password
)
from app.db.session import get_db
from app.models.organization import Organization
from app.models.session import Session
from app.models.user import User
from app.schemas.auth import (
    OrganizationRegister, RefreshRequest, TokenResponse, UserRegister
)

router = APIRouter(prefix="/auth", tags=["Auth"])

async def _create_session_and_tokens(
    db: AsyncSession, request: Request, *, 
    user_id: int | None = None, organization_id: int | None = None, 
    role: str, subject_id: int
) -> TokenResponse:
    """Вспомогательная функция: создает сессию в БД и выдает пару токенов."""
    refresh_token = generate_refresh_token()
    session = Session(
        user_id=user_id,
        organization_id=organization_id,
        refresh_token_hash=hash_refresh_token(refresh_token),
        user_agent=request.headers.get("user-agent", "")[:500] or None,
        ip_address=request.client.host if request.client else None,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(session)
    await db.commit()

    access_token = create_access_token(subject=str(subject_id), role=role)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/register/user", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_user(data: UserRegister, request: Request, db: AsyncSession = Depends(get_db)):
    # Проверка на дубликаты
    if (await db.execute(select(User.id).where(User.email == data.email))).scalar_one_or_none():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Этот e-mail уже используется")
    if (await db.execute(select(User.id).where(User.phone == data.phone))).scalar_one_or_none():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Этот номер уже используется")

    # Создание пользователя
    user = User(
        full_name=data.full_name, email=data.email, phone=data.phone,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return await _create_session_and_tokens(db, request, user_id=user.id, role="user", subject_id=user.id)


@router.post("/register/organization", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_organization(data: OrganizationRegister, request: Request, db: AsyncSession = Depends(get_db)):
    if (await db.execute(select(Organization.id).where(Organization.email == data.email))).scalar_one_or_none():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Этот e-mail уже используется")
    if (await db.execute(select(Organization.id).where(Organization.phone == data.phone))).scalar_one_or_none():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Этот номер уже используется")

    org = Organization(
        name=data.name, email=data.email, phone=data.phone,
        description=data.description, website=data.website,
        password_hash=hash_password(data.password),
    )
    db.add(org)
    await db.commit()
    await db.refresh(org)

    return await _create_session_and_tokens(db, request, organization_id=org.id, role="organization", subject_id=org.id)


@router.post("/login", response_model=TokenResponse)
async def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    identifier = form.username
    password = form.password

    user = (await db.execute(select(User).where(or_(User.email == identifier, User.phone == identifier)))).scalar_one_or_none()
    if user and verify_password(password, user.password_hash):
        return await _create_session_and_tokens(db, request, user_id=user.id, role="user", subject_id=user.id)

    org = (await db.execute(select(Organization).where(or_(Organization.email == identifier, Organization.phone == identifier)))).scalar_one_or_none()
    if org and verify_password(password, org.password_hash):
        return await _create_session_and_tokens(db, request, organization_id=org.id, role="organization", subject_id=org.id)

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Неправильные данные для входа")