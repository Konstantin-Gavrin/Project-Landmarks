from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from config.database import Base

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    landmark_id = Column(Integer, ForeignKey('landmarks.id'), nullable=False)
    
    user = relationship('User', back_populates='ratings')
    landmark = relationship('Landmark', back_populates='ratings')  # Обратная связь с Landmark
    
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )
