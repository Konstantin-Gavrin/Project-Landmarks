# middleware/authJWT.py

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from config.database import get_db
from sqlalchemy.orm import Session
from models.user import User
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

# Зависимость для извлечения и проверки токена
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Декодируем токен и извлекаем информацию
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Получаем пользователя из базы данных
        user = db.query(User).filter(User.username == username).first()
        
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
