from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base
from passlib.context import CryptContext

# Инициализация контекста для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'

    # Поля таблицы пользователя
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(30), nullable=False)  # Имя пользователя
    email = Column(String(100), nullable=False, unique=True)  # Уникальный email
    password = Column(String(255), nullable=False)  # Пароль пользователя

    # Связи с другими таблицами
    photos = relationship('Photo', back_populates='user', cascade='all, delete-orphan')
    ratings = relationship('Rating', back_populates='user', cascade='all, delete-orphan')
    landmarks = relationship('Landmark', back_populates='user', cascade='all, delete-orphan')

    # Метод для хеширования пароля
    def set_password(self, password: str):
        self.password = pwd_context.hash(password)
    
    # Метод для проверки пароля
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)
