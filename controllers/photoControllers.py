from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.photo import Photo
from config.database import get_db
from pydantic import BaseModel
from typing import List
from schemas.photo import PhotoBase, PhotoCreate
from middleware.authJWT import get_current_user
from models.user import User

router = APIRouter()

# Pydantic схема для фотографии
class PhotoBase(BaseModel):
    user_id: int
    landmark_id: int
    image_url: str  # Здесь предполагается, что есть поле для URL изображения

    model_config = {
        "from_attributes": True
    }


# Генерация CRUD операций
def generate_crud_operations(model):
    return {
        'create': lambda db, data: db.add(model(**data)) or db.commit(),
        'get_all': lambda db: db.query(model).all(),
        'get_one': lambda db, id: db.query(model).filter(model.id == id).first(),
        'update': lambda db, id, data: db.query(model).filter(model.id == id).update(data) or db.commit(),
        'delete': lambda db, id: db.query(model).filter(model.id == id).delete() or db.commit(),
    }

photo_crud = generate_crud_operations(Photo)

# Получение всех фотографий пользователя
@router.get("/user/{user_id}", response_model=List[PhotoBase])
async def get_photos_by_user(user_id: int, db: Session = Depends(get_db)):
    try:
        photos = db.query(Photo).filter(Photo.user_id == user_id).all()
        return photos
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Получение всех фотографий для достопримечательности
@router.get("/landmark/{landmark_id}", response_model=List[PhotoBase])
async def get_photos_by_landmark(landmark_id: int, db: Session = Depends(get_db)):
    try:
        photos = db.query(Photo).filter(Photo.landmark_id == landmark_id).all()
        return photos
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@router.get("/", response_model=List[PhotoBase])
async def get_all_photos(db: Session = Depends(get_db)):
    try:
        photos = db.query(Photo).all()
        return photos
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/{photo_id}", response_model=PhotoBase)
async def get_photo_by_id(photo_id: int, db: Session = Depends(get_db)):
    try:
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")
        return photo
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.post("/photos", response_model=PhotoCreate, tags=["Photos"])
async def create_photo(photo: PhotoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        new_photo = Photo(
            image_url = photo.image_url,
            landmark_id = photo.landmark_id,
            user_id=current_user.id
        )

        db.add(new_photo)
        db.commit()
        db.refresh(new_photo)

        return new_photo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/photos/{photo_id}", response_model=PhotoBase, tags=["Photos"])
async def update_photo(
    photo_id: int,
    photo: PhotoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ищем достопримечательность по ID
    db_photo = db.query(Photo).filter(Photo.id == photo_id).first()

    if not db_photo:
        raise HTTPException(status_code=404, detail="photo not found")
    
    # Проверяем, принадлежит ли достопримечательность текущему пользователю
    if db_photo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to edit this landmark")

    # Обновляем поля достопримечательности
    db_photo.image_url = photo.image_url,
    db_photo.landmark_id = photo.landmark_id

    # Сохраняем изменения в базе
    db.commit()
    db.refresh(db_photo)

    return db_photo
    
@router.delete("/photos/{photo_id}", tags=["Photos"])
async def delete_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ищем фотографию по ID
    db_photo = db.query(Photo).filter(Photo.id == photo_id).first()

    if not db_photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Проверяем, принадлежит ли фотография текущему пользователю
    if db_photo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this photo")

    # Удаляем запись из базы данных
    db.delete(db_photo)
    db.commit()

    return {"message": "Photo successfully deleted"}