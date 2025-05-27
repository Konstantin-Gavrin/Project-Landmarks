from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(200), nullable=False)  # Добавлено поле image_url
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    landmark_id = Column(Integer, ForeignKey('landmarks.id'), nullable=False)

    user = relationship('User', back_populates='photos')
    landmark = relationship('Landmark', back_populates='photos')
