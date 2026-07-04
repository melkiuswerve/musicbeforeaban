from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from src.models_db.user import User
from sqlalchemy import select
from src.backend.db import AsyncSession
JWT_SECRET: str = "85960eb992570f98ee107f6a895d5f51hjfehjwuhfgtywDFTFWD"
JWT_ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
REFRESH_TOKEN_EXPIRE_DAYS: int = 30
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Используйте pbkdf2_sha256 вместо bcrypt

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def authenticate_user(username: str, password: str, db: AsyncSession) -> User| None:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return None
    if not pwd_context.verify(password, user.password_hash):
        return None
    return user

