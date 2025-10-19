from src.exception.exception import PersonalizedCoachException
from src.logging.logger import logging
from src.contants import *
import os,sys
import joblib
import pandas as pd
from src.models.chatbot_retriver import ChatRetriever, Generative_Chatbot, Hybrid_Chatbot
from src.models.Nutrition_recommender import NutrientModel
from src.models.workout_recommender import WorkoutModel

class InferencePipeline:
    '''
    Unified inference pipeline:
    - Nutrition Recommender
    - Workout Recommender
    - Hybrid Chatbot
    '''
    def __init__(self):
        try:
            logging.info("Initilizing inference pipeline...")
            
            # Load Nutrition Model
            self.nutrition_model_path = os.path.join(NUTRITION_OUT,"nutrition_combined_model.joblib")
            self.nutrition_label_path = os.path.join(NUTRITION_OUT,"meal_label_encoder.joblib")
            
            self.nutrition_model = NutrientModel.load(self.nutrition_model_path)
            self.meal_encoder = joblib.load(self.nutrition_label_path)
            
            logging.info("Loaded Nutrition Recommender Model successfully...")
            
            # Load workout model
            self.workout_model_path = os.path.join(WORKOUT_OUT, "workout_combined_model.joblib")
            self.workout_label_path = os.path.join(WORKOUT_OUT, "workout_le.joblib")
            
            self.workout_model = WorkoutModel.load(self.workout_model_path)
            self.workout_encoder = joblib.load(self.workout_label_path)
            
            logging.info("Loaded Workout Recommender Model successfully...")
            
            # Load Hybrid Chatbot (Retriever + Generative)
            retriever = ChatRetriever().load(CHATBOT_OUT)
            generator = Generative_Chatbot(model_name="google/gemma-2-2b-it")
            self.chatbot = Hybrid_Chatbot(retriever=retriever, generator=generator)
            
            logging.info("Hybrid Chatbot Initialized successfully...")
        except PersonalizedCoachException as e:
            logging.info(f"Error while initializing Inference Pipeline: {e}")
            raise PersonalizedCoachException(e,sys)
        
    def recommend_nutrition(self, user_data:dict):
        try:
            user_df = pd.DataFrame([user_data])
            preds = self.nutrition_model.predict(user_df)
            
            # decode meal name
            for p in preds:
                p['meal']=self.meal_encoder.inverse_transform([int(p['meal'])])[0]
                
            logging.info("Nutrition recommendation completed...")
            return preds[0]
        
        except PersonalizedCoachException as e:
            logging.info(f"Error during Nutrition inference: {e}")
            raise PersonalizedCoachException(e,sys) 

    def recommend_workout(self, user_data:dict):
        try:
            user_df = pd.DataFrame([user_data])
            preds = self.workout_model.predict(user_df)
            
            # decode workout name
            for p in preds:
                p['workout'] = self.workout_encoder.inverse_transform([int(p['workout'])])[0]

            logging.info("Workout recommendation completed...")
            return preds[0]
        except PersonalizedCoachException as e:
            logging.info(f"Error during Workout inference: {e}")
            
    def chat_with_bot(self, query:str):
        try:
            response = self.chatbot.chat(query)
            return response
        except PersonalizedCoachException as e:
            logging.info(f"Error during ChatBot inference: {e}")
            raise PersonalizedCoachException(e,sys)
        
if __name__=="__main__":
    try:
        inference = InferencePipeline()
         # Example 1: Nutrition Prediction
        nutrition_input = {
            'age': 28,
            'gender': 'female',
            'bmi': 22.4,
            'goal': 'muscle_gain',
            'diet_type': 'vegetarian'
        }
        nutrition_reco = inference.recommend_nutrition(nutrition_input)
        print("\n🧠 Nutrition Recommendation:\n", nutrition_reco)
        
         # Example 2: Workout Prediction
        workout_input = {
            'intensity': 'high',
            'muscle_group': 'legs',
            'age': 28,
            'gender': 'female',
            'goal': 'muscle_gain',
            'bmi': 22.4,
            'fitness_level': 'advanced'
        }
        workout_reco = inference.recommend_workout(workout_input)
        print("\n🏋️ Workout Recommendation:\n", workout_reco)
        
        
        # Example 3: Chatbot Response
        query = "What is bmi?"
        bot_response = inference.chat_with_bot(query)
        print("\n🤖 Chatbot Response:\n", bot_response)
        
    except PersonalizedCoachException as e:
        raise PersonalizedCoachException(e,sys)