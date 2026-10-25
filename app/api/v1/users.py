from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.security import hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import AccountDeleteRequest, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Вернуть данные текущего пользователя."""
    return current_user


@router.patch("/me", response_model=UserRead)
async def update_my_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Обновление данных пользователя (PATCH)."""
    
    # 1. Если пользователь пытается сменить пароль или контакты — требуем текущий пароль
    is_sensitive_change = data.password or data.email or data.phone
    if is_sensitive_change:
        if not data.current_password or not verify_password(data.current_password, current_user.password_hash):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Неверный текущий пароль")

    # 2. Проверка уникальности нового email
    if data.email and data.email != current_user.email:
        if (await db.execute(select(User.id).where(User.email == data.email))).scalar_one_or_none():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Этот e-mail уже используется")
        current_user.email = data.email

    # 3. Проверка уникальности нового телефона
    if data.phone and data.phone != current_user.phone:
        if (await db.execute(select(User.id).where(User.phone == data.phone))).scalar_one_or_none():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Этот номер уже используется")
        current_user.phone = data.phone

    # 4. Обновление обычных полей
    if data.full_name:
        current_user.full_name = data.full_name

    # 5. Обновление пароля (совпадение паролей уже проверено в Pydantic!)
    if data.password:
        current_user.password_hash = hash_password(data.password)

    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(
    data: AccountDeleteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Удаление аккаунта пользователя (DELETE)."""
    # Проверяем пароль перед удалением
    if not verify_password(data.password, current_user.password_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Неверный пароль")

    # Удаляем пользователя. 
    # Благодаря ondelete="CASCADE" в модели Session, все его сессии удалятся сами.
    await db.delete(current_user)
    await db.commit()