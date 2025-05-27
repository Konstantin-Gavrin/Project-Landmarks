from pydantic import BaseModel

class RatingBase(BaseModel):
    rating: int
    user_id: int
    landmark_id: int

    model_config = {
        "from_attributes": True
    }
