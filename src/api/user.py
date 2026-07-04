from sqlalchemy import select, delete
from fastapi import APIRouter, HTTPException, status, Depends
from src.schemas.example import UserCreate
from src.backend.db import  AsyncSession
from src.models_db.user import User
from src.core.security import get_current_user
from src.core.settings import get_password_hash
from src.backend.db import get_db


router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me")
async def read_profile(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user,
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password_hash),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {
        "username": new_user.username,
        "email": new_user.email,

    }


@router.delete("/me")
async def delete_account(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    # Получаем пользователя с блокировкой строки для избежания race conditions
    result = await db.execute(
        select(User).where(User.id == current_user.id).with_for_update()
    )
    user_in_db = result.scalar_one_or_none()

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user_name = user_in_db.name
    # Удаляем пользователя
    await db.delete(user_in_db)
    await db.commit()

    return {"message": f"Account {user_name} permanently deleted"}