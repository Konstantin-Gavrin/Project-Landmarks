from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from config.database import Base  # Импортируем Base из config/database.py

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    photos = relationship('Photo', back_populates='user', cascade='all, delete-orphan')
    ratings = relationship('Rating', back_populates='user', cascade='all, delete-orphan')
    landmarks = relationship('Landmark', back_populates='user', cascade='all, delete-orphan')

class Landmark(Base):
    __tablename__ = 'landmarks'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship('User', back_populates='landmarks')
    photos = relationship('Photo', back_populates='landmark', cascade='all, delete-orphan')
    ratings = relationship('Rating', back_populates='landmark', cascade='all, delete-orphan')

class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    landmark_id = Column(Integer, ForeignKey('landmarks.id'))
    
    user = relationship('User', back_populates='photos')
    landmark = relationship('Landmark', back_populates='photos')

class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    landmark_id = Column(Integer, ForeignKey('landmarks.id'))
    score = Column(Integer, nullable=False)
    
    user = relationship('User', back_populates='ratings')
    landmark = relationship('Landmark', back_populates='ratings')
