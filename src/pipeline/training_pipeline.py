from src.custom_logging.logger import logging
from src.exception.exception import PersonalizedCoachException
from src.contants import *
import os, sys
import joblib
import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import mlflow
import mlflow.sklearn
import dagshub
from dotenv import load_dotenv
load_dotenv()
dagshub.init(repo_owner='samarthchugh', repo_name='AI---Personalized-Workout-Nutrition-Coach', mlflow=True)
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME"))

from src.models.Nutrition_recommender import NutrientModel, NutritionRecommender
from src.models.workout_recommender import WorkoutModel, WorkoutRecommender
from src.models.chatbot_retriver import ChatRetriever

class TrainingPipeline:
    def __init__(self):
        # DATA
        self.nutrition_csv=NUTRITION_PATH
        self.workout_csv=WORKOUT_PATH
        self.faq_csv=FAQ_PATH
        
        # OUTPUT DIR
        self.nutrition_out=NUTRITION_OUT
        self.workout_out=WORKOUT_OUT
        self.chatbot_out=CHATBOT_OUT
        
    def train_nutrition(self):
        try:
            # mlflow.set_experiment("Nutrition-Recommender")

            df = pd.read_csv(self.nutrition_csv)
            feature_cols = ['age','gender','bmi','goal','diet_type']
            target_meal = 'meal_name'
            target_nutrients = ['calories','protein_g','fats_g','carbs_g']
            
            X = df[feature_cols]
            y_meal = df[target_meal]
            y_nutrients = df[target_nutrients]
            
            # encode meal labels
            meal_le = LabelEncoder()
            y_meal_enc = meal_le.fit_transform(y_meal.astype(str))

            # split data
            X_train, X_test, y_meal_train, y_meal_test, y_nutrients_train, y_nutrients_test = train_test_split(X, y_meal_enc, y_nutrients, 
                                                                                            test_size=TRAIN_TEST_SPLIT_RATIO, random_state=RANDOM_STATE
            )
            logging.info("Data split completed...")
            
            # model initialization
            nutrition_model = NutritionRecommender()
            logging.info("Training of Nutrition model started...")
            # train model
            with mlflow.start_run(run_name="nutrition_training"):
                mlflow.log_param("n_sample", len(df))
                mlflow.log_param("model_type", "RandomForest + MultiOutputRegressor")
                
                nutrition_model.fit(X_train,y_meal_train,y_nutrients_train)
                
                # Evaluate
                meal_pred = nutrition_model.predict_meal(X_test)
                nutrients_pred = nutrition_model.predict_nutrients(X_test)
                
                meal_acc = accuracy_score(y_meal_test, meal_pred)
                mlflow.log_metric("meal_accuracy",float(meal_acc))
                
                nutrients_maes={}
                for i, col in enumerate(target_nutrients):
                    mae = mean_absolute_error(y_nutrients_test[col],nutrients_pred[:,i])
                    nutrients_maes[col] = float(mae)
                    mlflow.log_metric(f"mae_{col}", float(mae))
                    
                # Save artifacts
                os.makedirs(self.nutrition_out,exist_ok=True)
                
                # save label encoder
                meal_le_path = os.path.join(self.nutrition_out, 'meal_label_encoder.joblib')
                joblib.dump(meal_le, meal_le_path)
                
                # save combined model
                combined = NutrientModel(
                    meal_model = nutrition_model.meal_pipeline,
                    nutrients_model = nutrition_model.nutrients_pipeline
                )
                combined_path = os.path.join(self.nutrition_out, "nutrition_combined_model.joblib")
                combined.save(combined_path)
                
                # log artifacts
                mlflow.log_artifact(meal_le_path)
                mlflow.log_artifact(combined_path)
            print(f"Nutrition model trained and saved! Meal acc: {meal_acc:.3f}")
            return combined
        except PersonalizedCoachException as e:
            logging.info("Error occur in train_nutrition function: ",e)
            raise PersonalizedCoachException(e,sys)
        
    def train_workout(self):
        try:
            # mlflow.set_experiment("Workout-Recommender")
            df = pd.read_csv(self.workout_csv)
            feature_cols = ['intensity','muscle_group','age','gender','goal','bmi','fitness_level']
            target_workout_name = 'name'
            target_duration = 'duration_min'
            
            X = df[feature_cols]
            y_workout_name = df[target_workout_name]
            y_duration = df[target_duration]

            workout_enc = LabelEncoder()
            y_workout_enc = workout_enc.fit_transform(y_workout_name.astype(str))
            
            X_train, X_test, y_workout_train, y_workout_test, y_duration_train, y_duration_test = train_test_split(X, y_workout_enc, y_duration,
                                                                                                    test_size=TRAIN_TEST_SPLIT_RATIO, random_state=RANDOM_STATE
            )
            logging.info("Data split completed...")
            
            # model initialization
            workout_model = WorkoutRecommender()
            logging.info("Workout-Recommender-Model training started...")
            # model training
            with mlflow.start_run(run_name="workout_training"):
                mlflow.log_param("n_sample",len(df))
                mlflow.log_param("model_type","RandomForest_Classifier + RandomForest_Regressor")
                
                workout_model.fit(X_train,y_workout_train,y_duration_train)
                
                # evaluate
                workout_pred = workout_model.predict_workout(X_test)
                duration_pred = workout_model.predict_duration(X_test)
                
                workout_acc = accuracy_score(y_workout_test, workout_pred)
                mlflow.log_metric("Workout-Accuracy",float(workout_acc))

                duration_mae = mean_absolute_error(y_duration_test, duration_pred)
                mlflow.log_metric("Duration-MAE", float(duration_mae))
                
                # save artifacts
                os.makedirs(self.workout_out, exist_ok=True)
                
                # save label encoder
                workout_le_path = os.path.join(self.workout_out, 'workout_le.joblib')
                joblib.dump(workout_enc,workout_le_path)
                
                # save combined model
                combined = WorkoutModel(
                    workout_model=workout_model.workout_pipeline,
                    duration_model=workout_model.duration_pipeline
                )
                combined_path = os.path.join(self.workout_out,"workout_combined_model.joblib")
                combined.save(combined_path)
                
                # log artifacts
                mlflow.log_artifact(workout_le_path)
                mlflow.log_artifact(combined_path)
            print(f"Workout model trained and saved! workout acc: {workout_acc:.3f}")
            return combined
        except PersonalizedCoachException as e:
            logging.info("Error occur in train_workout function: ",e)
            raise PersonalizedCoachException(e,sys)
        
    def train_retrievel_chatbot(self):
        try:
            # mlflow.set_experiment("ChatBot-Retriever")
            df = pd.read_csv(self.faq_csv)
            # expect columns ['question','answer']
            if not {'question','answer'}.issubset(set(df.columns)):
                raise ValueError("FAQ CSV must contain 'question' and 'answer' columns")
            
            chatbot = ChatRetriever(device='cpu')
            logging.info("Training Retrievel Chatbot...")
            chatbot.fit(df,question_col='question', answer_col='answer', n_neighbors=6)
            
            os.makedirs(CHATBOT_OUT, exist_ok=True)
            chatbot.save(CHATBOT_OUT)
            
            # Log artifacts under mlflow
            with mlflow.start_run(run_name="chatbot_retriever_build"):
                mlflow.log_param("n_faqs", len(df))
                # log embeddings file & faq csv & nn file & embedder (these are in CHATBOT_OUT)
                mlflow.log_artifact(os.path.join(CHATBOT_OUT, 'faq_data.csv'))
                mlflow.log_artifact(os.path.join(CHATBOT_OUT, 'faq_embeddings.npy'))
                mlflow.log_artifact(os.path.join(CHATBOT_OUT, 'nn.joblib'))
                mlflow.log_artifact(os.path.join(CHATBOT_OUT, 'embedder_name.txt'))
            print("Chatbot retriever built and saved.")
            return chatbot
        except PersonalizedCoachException as e:
            logging.info(f"Error occured in train_retrievel_chatbot function: {e}")
            raise PersonalizedCoachException(e,sys)
        

    def initiate_training(self):
        try:
            logging.info("Initiate Training ....")
            self.train_nutrition()
            print("Nutrition Model Trained...")
            self.train_workout()
            print("Workout Model Trained...")
            self.train_retrievel_chatbot()
            print("Retriever ChatBot Trained...")
        except PersonalizedCoachException as e:
            logging.info(f"error in initiating the model training: {e}")
            raise PersonalizedCoachException(e,sys)
            


# def main():
#     try:
#         trainer=TrainingPipeline()
#         trainer.train_nutrition()
#         print("Nutrition Model Trained...")
#         trainer.train_workout()
#         print("Workout Model Trained...")
#         trainer.train_retrievel_chatbot()
#         print("Retriever ChatBot Trained...")
#     except PersonalizedCoachException as e:
#         raise PersonalizedCoachException(e,sys)
    
if __name__=="__main__":
    trainer=TrainingPipeline().initiate_training()
    print(trainer)