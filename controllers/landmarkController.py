from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from models.landmarks import Landmark
from schemas.landmarks import LandmarkBase, LandmarkCreate
from middleware.authJWT import get_current_user  # Импортируем зависимость для токена
from models.user import User


router = APIRouter()

# Получение всех достопримечательностей для пользователя
@router.get("/landmarks/user/{user_id}", response_model=List[LandmarkBase], tags=["Landmarks"])
async def find_landmarks_by_user(user_id: int, db: Session = Depends(get_db)):
    landmarks = db.query(Landmark).filter(Landmark.user_id == user_id).all()
    if not landmarks:
        raise HTTPException(status_code=404, detail="No landmarks found for this user")
    return landmarks


@router.get("/landmarks/{landmark_id}", response_model=LandmarkBase, tags=["Landmarks"])
async def get_landmark_by_id(landmark_id: int, db: Session = Depends(get_db)):
    # Ищем достопримечательность по ID
    db_landmark = db.query(Landmark).filter(Landmark.id == landmark_id).first()

    if not db_landmark:
        raise HTTPException(status_code=404, detail="Landmark not found")
    
    return db_landmark


# Получение всех достопримечательностей для страны
@router.get("/landmarks/country/{country}", response_model=List[LandmarkBase], tags=["Landmarks"])
async def find_landmarks_by_country(country: str, db: Session = Depends(get_db)):
    landmarks = db.query(Landmark).filter(Landmark.country == country).all()
    if not landmarks:
        raise HTTPException(status_code=404, detail="No landmarks found in this country")
    return landmarks

@router.get("/", response_model=List[LandmarkBase])
async def get_all_landmarks(db: Session = Depends(get_db)):
    landmarks = db.query(Landmark).all()
    return landmarks

@router.post("/landmarks", response_model=LandmarkCreate, tags=["Landmarks"])
async def create_landmark(landmark: LandmarkCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        
        # Создаем новый объект Landmark с данными из тела запроса
        new_landmark = Landmark(
        name=landmark.name,
        description=landmark.description,
        location=landmark.location,
        country=landmark.country,
        image_url=landmark.image_url,
        user_id=current_user.id  # Безопасно: взято из токена
        )
 
        # Добавляем новую достопримечательность в базу данных
        db.add(new_landmark)
        db.commit()  # Сохраняем изменения в базе данных
        db.refresh(new_landmark)  # Обновляем объект с новыми данными

        return new_landmark
    except Exception as e:
        db.rollback()  # В случае ошибки откатываем изменения
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/landmarks/{landmark_id}", response_model=LandmarkBase, tags=["Landmarks"])
async def update_landmark(
    landmark_id: int,
    landmark: LandmarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ищем достопримечательность по ID
    db_landmark = db.query(Landmark).filter(Landmark.id == landmark_id).first()

    if not db_landmark:
        raise HTTPException(status_code=404, detail="Landmark not found")
    
    # Проверяем, принадлежит ли достопримечательность текущему пользователю
    if db_landmark.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to edit this landmark")

    # Обновляем поля достопримечательности
    db_landmark.name = landmark.name
    db_landmark.description = landmark.description
    db_landmark.location = landmark.location
    db_landmark.country = landmark.country
    db_landmark.image_url = landmark.image_url

    # Сохраняем изменения в базе
    db.commit()
    db.refresh(db_landmark)

    return db_landmark


@router.delete("/landmarks/{landmark_id}", tags=["Landmarks"])
async def delete_landmark(
    landmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ищем достопримечательность по ID
    db_landmark = db.query(Landmark).filter(Landmark.id == landmark_id).first()

    if not db_landmark:
        raise HTTPException(status_code=404, detail="Landmark not found")

    # Проверяем, принадлежит ли она текущему пользователю
    if db_landmark.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this landmark")

    # Удаляем достопримечательность
    db.delete(db_landmark)
    db.commit()

    return {"message": "Landmark successfully deleted"}