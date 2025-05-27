from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Landmark(Base):
    __tablename__ = 'landmarks'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(100), nullable=True)
    country = Column(String(50), nullable=True)
    image_url = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    user = relationship('User', back_populates='landmarks')
    photos = relationship('Photo', back_populates='landmark', cascade='all, delete-orphan')
    ratings = relationship('Rating', back_populates='landmark', cascade='all, delete-orphan')  # Добавьте эту строку
