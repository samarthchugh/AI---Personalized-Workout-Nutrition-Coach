from pydantic import BaseModel

class NutritionInput(BaseModel):
    age:int
    gender: str
    bmi: float
    goal: str
    diet_type: str
    
class WorkoutInput(BaseModel):
    intensity: str
    muscle_group: str
    age: int
    gender: str
    goal: str
    bmi: float
    fitness_level: str
    
class ChatInput(BaseModel):
    query: str