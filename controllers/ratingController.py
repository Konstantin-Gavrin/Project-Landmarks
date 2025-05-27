from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.rating import Rating
from config.database import get_db
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Pydantic схема для рейтинга
class RatingBase(BaseModel):
    rating: int
    user_id: int
    landmark_id: int

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

rating_crud = generate_crud_operations(Rating)

# Получение всех рейтингов пользователя
@router.get("/user/{user_id}", response_model=List[RatingBase])
async def get_ratings_by_user(user_id: int, db: Session = Depends(get_db)):
    try:
        ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
        return ratings
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Получение всех рейтингов для достопримечательности
@router.get("/landmark/{landmark_id}", response_model=List[RatingBase])
async def get_ratings_by_landmark(landmark_id: int, db: Session = Depends(get_db)):
    try:
        ratings = db.query(Rating).filter(Rating.landmark_id == landmark_id).all()
        return ratings
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/", response_model=List[RatingBase])
async def get_all_ratings(db: Session = Depends(get_db)):
    try:
        ratings = db.query(Rating).all()
        return ratings
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/{rating_id}", response_model=RatingBase)
async def get_rating_by_id(rating_id: int, db: Session = Depends(get_db)):
    try:
        rating = db.query(Rating).filter(Rating.id == rating_id).first()
        if not rating:
            raise HTTPException(status_code=404, detail="Rating not found")
        return rating
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

