from sqlalchemy.orm import Session
from config.database import engine, SessionLocal
from models.user import User
from models.landmarks import Landmark
from models.photo import Photo
from models.rating import Rating
from config.database import Base  # Если Base определен в другом файле
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

# Создание таблиц
def create_tables():
    Base.metadata.create_all(bind=engine)

# Функция для добавления начальных данных
def create_initial_data():
    db = SessionLocal()
    try:
        # Хеширование паролей
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash("user1_123")

        # Создание пользователей
        user1 = User(username="user1", email="user1@example.com", password=hashed_password)
        user2 = User(username="user2", email="user2@example.com", password=hashed_password)
        
        db.add(user1)
        db.add(user2)
        
        db.commit()  # Важно сделать commit, чтобы сгенерировались id для пользователей

        # После commit() у пользователей появятся id
        db.refresh(user1)
        db.refresh(user2)

        # Создание достопримечательностей
        landmark1 = Landmark(
            name="Eiffel Tower",
            description="The design of the Eiffel Tower is attributed to Maurice Koechlin and Émile Nouguier, two senior engineers working for the Compagnie des Établissements Eiffel. It was envisaged after discussion about a suitable centerpiece for the proposed 1889 Exposition Universelle, a world's fair to celebrate the centennial of the French Revolution.",
            location="Paris",
            country="France",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg/250px-Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg",
            user_id=user1.id  # Связь с пользователем
        )
        
        db.add(landmark1)
        db.commit()  # Коммит, чтобы сгенерировался id для landmark1
        
        db.refresh(landmark1)  # Получаем id для достопримечательности после commit()

        # Добавление фотографий
        photo1 = Photo(
            user_id=user1.id, 
            landmark_id=landmark1.id,
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg/250px-Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg"  # URL фотографии
        )
        db.add(photo1)


        # Добавление рейтингов
        rating1 = Rating(rating=5, user_id=user1.id, landmark_id=landmark1.id)
        db.add(rating1)

        db.commit()  # Коммит всех изменений в базу данных

        # Получаем объекты с базы
        db.refresh(landmark1)
        db.refresh(photo1)
        db.refresh(rating1)

        print("Initial data added successfully.")

    except IntegrityError as e:
        db.rollback()
        print(f"Error: {e.orig}")
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()  # Создание таблиц
    create_initial_data()  # Добавление начальных данных
