from pydantic import BaseModel

class PhotoCreate(BaseModel):
    image_url: str
    landmark_id: int



class PhotoBase():
    id: int

    model_config = {
        "from_attributes": True  
    }
