from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from config.database import get_db
import bcrypt
import jwt
from pydantic import BaseModel
import os
from datetime import datetime, timedelta
from typing import List
from schemas.user import UserBase



SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни токена (30 минут)

router = APIRouter()

# Схема для входа
class SignIn(BaseModel):
    username: str
    password: str

# Схема для регистрации
class SignUp(BaseModel):
    username: str
    email: str
    password: str


# Генерация CRUD операций
def generate_crud_operations(model):
    return {
        'create': lambda db, data: db.add(model(**data)) or db.commit(),
        'get_all': lambda db: db.query(model).all(),
        'get_one': lambda db, id: db.query(model).filter(model.id == id).first(),
        'update': lambda db, id, data: db.query(model).filter(model.id == id).update(data) or db.commit(),
        'delete': lambda db, id: db.query(model).filter(model.id == id).delete() or db.commit(),
    }

user_crud = generate_crud_operations(User)

# Метод для получения пользователей по имени пользователя
@router.get("/username/{username}")
async def get_users_by_username(username: str, db: Session = Depends(get_db)):
    try:
        users = db.query(User).filter(User.username == username).all()
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Функция для создания JWT токена с истечением
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup")
async def signup(sign_up_data: SignUp, db: Session = Depends(get_db)):
    try:
        # Проверка, существует ли уже пользователь с таким же именем или email
        existing_user = db.query(User).filter((User.username == sign_up_data.username) | (User.email == sign_up_data.email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email is already taken")

        # Хэширование пароля перед сохранением
        hashed_password = bcrypt.hashpw(sign_up_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Создание нового пользователя и добавление в базу данных
        new_user = User(username=sign_up_data.username, email=sign_up_data.email, password=hashed_password)
        db.add(new_user)
        db.commit()

        return {"message": "User successfully registered", "username": new_user.username}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="User registration failed")


# Метод для входа пользователя
@router.post("/signin")
async def signin(sign_in_data: SignIn, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.username == sign_in_data.username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Проверка пароля с использованием bcrypt
        is_match = bcrypt.checkpw(sign_in_data.password.encode('utf-8'), user.password.encode('utf-8'))
        if not is_match:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Генерация JWT токена
        access_token = create_access_token(data={"sub": user.username})
        return {"message": "Authentication successful", "access_token": access_token, "token_type": "bearer"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="User login failed")

@router.get("/", response_model=List[UserBase])
async def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
@router.get("/{user_id}", response_model=UserBase)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
