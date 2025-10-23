from fastapi import FastAPI, HTTPException, Depends, APIRouter
from src.pydantic_models import NutritionInput, WorkoutInput, ChatInput
from src.pipeline.inference_pipeline import InferencePipeline
from sqlalchemy.orm import sessionmaker, Session
from src.db.models import base, Workout, Nutrition, FAQ
from src.db.connection import get_engine
from src.custom_logging.logger import logging
from src.exception.exception import PersonalizedCoachException
import uvicorn

app = FastAPI(
    title="Personalized Coach API",
    description="Unified API for Nutrition, Workout, and Chatbot Recommendations",
    version='1.0.0'
)

# create DB engine and session
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base.metadata.create_all(bind=engine)

# dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize inference pipeline
inference = InferencePipeline()

# api endpoints
@app.get('/')
def root():
    return {'message':"Welcome to the Personalized Coach API🚀"}

# Nutrition Recommendation Endpoint
@app.post('/recommend/nutrition')
def recommend_nutrition(input_data: NutritionInput, db: Session = Depends(get_db)):
    try:
        logging.info("Received nutrition recommendation request...")
        result = inference.recommend_nutrition(input_data.dict())

        # Save to database
        nutrition_entry = Nutrition(
            meal_name=result.get("meal"),
            calories=result.get("calories"),
            protein_g=result.get("protein_g"),
            carbs_g=result.get("carbs_g"),
            fats_g=result.get("fats_g"),
            age=input_data.age,
            gender=input_data.gender,
            bmi=input_data.bmi,
            goal=input_data.goal,
            diet_type=input_data.diet_type,
        )
        db.add(nutrition_entry)
        db.commit()
        db.refresh(nutrition_entry)

        return {
            "status": "success",
            "data": result,
            "db_id": nutrition_entry.id
        }

    except PersonalizedCoachException as e:
        logging.error(f"Error in nutrition endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# Workout Recommendation Endpoint
@app.post("/recommend/workout")
def recommend_workout(input_data:WorkoutInput, db: Session = Depends(get_db)):
    try:
        logging.info("Received workout recommendation request...")
        result = inference.recommend_workout(input_data.dict())

        # Save to database
        workout_entry = Workout(
            name=result["workout"],
            duration_min=result["duration"],
            intensity=input_data.intensity,
            muscle_group=input_data.muscle_group,
            age=input_data.age,
            gender=input_data.gender,
            goal=input_data.goal,
            bmi=input_data.bmi,
            fitness_level=input_data.fitness_level,
        )
        db.add(workout_entry)
        db.commit()
        db.refresh(workout_entry)

        return {
            "status": "success",
            "data": result,
            "db_id": workout_entry.id
        }

    except PersonalizedCoachException as e:
        logging.error(f"Error in workout endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# Chatbot Endpoint
@app.post("/chat")
def chatbot_chat(query: ChatInput):
    try:
        logging.info("Chatbot query recieved...")
        response = inference.chat_with_bot(query.query)
        return {"query":query.query, "response":response}
    except PersonalizedCoachException as e:
        logging.error(f"Error in Chatbot endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# Retreive stored recommendations (for ETL)
@app.get("/data/nutrition")
def get_all_nutrition_records(db:Session=Depends(get_db)):
    records = db.query(Nutrition).all()
    return {'count':len(records), 'data':records}

@app.get("/data/workout")
def get_all_workout_records(db:Session=Depends(get_db)):
    records = db.query(Workout).all()
    return {'count':len(records), 'data':records} 

if __name__=="__main__":
    uvicorn.run("src.API.main:app", host="0.0.0.0", port=8000, reload=True)    

