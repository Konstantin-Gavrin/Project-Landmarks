from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic
from pydantic import BaseModel
from config.database import get_db

T = TypeVar("T", bound=BaseModel)

class CRUDController(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
        self.router = APIRouter()
        self.router.add_api_route("/", self.create, methods=["POST"])
        self.router.add_api_route("/", self.find_all, methods=["GET"])
        self.router.add_api_route("/{id}", self.find_one, methods=["GET"])
        self.router.add_api_route("/{id}", self.update, methods=["PUT"])
        self.router.add_api_route("/{id}", self.delete, methods=["DELETE"])
    
    async def create(self, item: T, db: Session = Depends(get_db)):
        db_item = self.model(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    async def find_all(self, db: Session = Depends(get_db)):
        return db.query(self.model).all()
    
    async def find_one(self, id: int, db: Session = Depends(get_db)):
        item = db.query(self.model).filter(self.model.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    
    async def update(self, id: int, item: T, db: Session = Depends(get_db)):
        db_item = db.query(self.model).filter(self.model.id == id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    async def delete(self, id: int, db: Session = Depends(get_db)):
        db_item = db.query(self.model).filter(self.model.id == id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(db_item)
        db.commit()
        return {"message": "Item deleted"}
