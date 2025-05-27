from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

    model_config = {
        "from_attributes": True
    }