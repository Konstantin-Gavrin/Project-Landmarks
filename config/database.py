from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # Используйте новый импорт
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

# Настройка базы данных
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
DB_DIALECT = os.getenv('DB_DIALECT')

# Формируем строку подключения
DATABASE_URL = f"{DB_DIALECT}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Создаем engine
engine = create_engine(DATABASE_URL)  # Удалено `check_same_thread=False`, так как это не нужно для MySQL

# Создаем sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем Base
Base = declarative_base()  # Это необходимо для определения моделей

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
