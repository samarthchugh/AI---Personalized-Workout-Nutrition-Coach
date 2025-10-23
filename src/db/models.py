## schema for db
from src.custom_logging.logger import logging
from src.exception.exception import PersonalizedCoachException
from src.contants import WORKOUTS_TABLE_NAME, NUTRITION_TABLE_NAME, FAQ_TABLE_NAME
import sys

from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class Workout(base):
    __tablename__ = WORKOUTS_TABLE_NAME
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    duration_min = Column(Float, nullable=False)
    intensity = Column(String(50), nullable=False)
    muscle_group = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    goal = Column(String(100), nullable=False)
    bmi = Column(Float, nullable=False)
    fitness_level = Column(String(100), nullable=False)
    
class Nutrition(base):
    __tablename__ = NUTRITION_TABLE_NAME
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    meal_name = Column(String(100), nullable=False)
    calories = Column(Float, nullable=False)
    protein_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)
    fats_g = Column(Float, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    bmi = Column(Float, nullable=False)
    goal = Column(String(100), nullable=False)
    diet_type = Column(String(100), nullable=False)
    
class FAQ(base):
    __tablename__ = FAQ_TABLE_NAME
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)