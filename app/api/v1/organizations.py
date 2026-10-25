from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_organization
from app.core.security import hash_password, verify_password
from app.db.session import get_db
from app.models.organization import Organization
from app.schemas.auth import (
    AccountDeleteRequest, OrganizationRead, OrganizationUpdate
)

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/me", response_model=OrganizationRead)
async def get_my_organization(current_org: Organization = Depends(get_current_organization)):
    """Вернуть данные текущей организации."""
    return current_org


@router.patch("/me", response_model=OrganizationRead)
async def update_my_organization(
    data: OrganizationUpdate,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    """Обновление данных организации (PATCH)."""
    
    # 1. Если пытаемся сменить пароль или контакты — требуем текущий пароль
    is_sensitive_change = data.password or data.email or data.phone
    if is_sensitive_change:
        if not data.current_password or not verify_password(data.current_password, current_org.password_hash):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Неверный текущий пароль")

    # 2. Проверка уникальности нового email
    if data.email and data.email != current_org.email:
        if (await db.execute(select(Organization.id).where(Organization.email == data.email))).scalar_one_or_none():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Этот e-mail уже используется")
        current_org.email = data.email

    # 3. Проверка уникальности нового телефона
    if data.phone and data.phone != current_org.phone:
        if (await db.execute(select(Organization.id).where(Organization.phone == data.phone))).scalar_one_or_none():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Этот номер уже используется")
        current_org.phone = data.phone

    # 4. Обновление обычных полей
    if data.name:
        current_org.name = data.name
        
    # Для текстовых полей используем is not None, чтобы можно было очистить их, передав пустую строку ""
    if data.description is not None:
        current_org.description = data.description
    if data.website is not None:
        current_org.website = data.website

    # 5. Обновление пароля (совпадение паролей уже проверено в Pydantic!)
    if data.password:
        current_org.password_hash = hash_password(data.password)

    await db.commit()
    await db.refresh(current_org)
    return current_org


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_organization(
    data: AccountDeleteRequest,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    """Удаление аккаунта организации (DELETE)."""
    if not verify_password(data.password, current_org.password_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Неверный пароль")

    await db.delete(current_org)
    await db.commit()