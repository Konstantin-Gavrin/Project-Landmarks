from fastapi import FastAPI
from config.createtables import create_tables

# Создание таблиц
create_tables()

from controllers.landmarkController import router as landmark_router
from controllers.userController import router as user_router
from controllers.photoControllers import router as photo_router
from controllers.ratingController import router as rating_router

app = FastAPI()

app.include_router(landmark_router, prefix="/landmarks", tags=["Landmarks"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(photo_router, prefix="/photos", tags=["Photos"])
app.include_router(rating_router, prefix="/ratings", tags=["Ratings"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Landmark API!"}
