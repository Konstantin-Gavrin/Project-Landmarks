from pydantic import BaseModel

# Схема для создания достопримечательности
class LandmarkCreate(BaseModel):
    name: str
    description: str
    location: str
    country: str
    image_url: str


# Схема для вывода достопримечательности
class LandmarkBase(LandmarkCreate):
    id: int  # ID записи в базе данных

    model_config = {
        "from_attributes": True
    }
