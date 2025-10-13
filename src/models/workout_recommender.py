from src.exception.exception import PersonalizedCoachException
from src.logging.logger import logging
import os
import sys
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

class WorkoutRecommender:
    """
    Workout model wrapper:
    - workout_pipeline: classifier that predicts the workout
    - duration_pipeline: regressor for predicting the duration of workout
    Both pipelines include a ColumnTransformer with numeric imputer + scaler and categorical features.
    """
    
    def __init__(self, categorical_features=None, numeric_features=None, random_state=42):
        self.categorical_features = categorical_features or ['intensity', 'muscle_group', 'gender', 'goal', 'fitness_level']
        self.numeric_features = numeric_features or ['age', 'bmi']
        self.random_state = random_state
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat',OneHotEncoder(handle_unknown='ignore',sparse_output=False),self.categorical_features),
                ('num',Pipeline(steps=[
                    ('imputer',KNNImputer(n_neighbors=5)),
                    ('scaler',StandardScaler())
                ]),self.numeric_features)
            ], remainder='drop',
            verbose_feature_names_out=False
        )
        
        self.workout_pipeline = Pipeline(
            steps=[
                ('preprocessor',preprocessor),
                ('classifier', RandomForestClassifier(n_estimators=200,random_state=self.random_state))
            ]
        )
        
        self.duration_pipeline = Pipeline(
            steps=[
                ('preprocessor',preprocessor),
                ('regressor', RandomForestRegressor(n_estimators=200, random_state=self.random_state))
            ]
        )
        
    def fit(self, X, y_workout, y_duration):
        try:
            self.workout_pipeline.fit(X,y_workout)
            self.duration_pipeline.fit(X, y_duration)
        except PersonalizedCoachException as e:
            logging.info(f"Erro while fitting the data: {e}")
            raise PersonalizedCoachException(e,sys)
        
    def predict_workout(self, X):
        try:
            return self.workout_pipeline.predict(X)
        except PersonalizedCoachException as e:
            logging.info(f"error while predicting workout: {e}")
            raise PersonalizedCoachException(e,sys)
        
    def predict_duration(self, X):
        try:
            return self.duration_pipeline.predict(X)
        except PersonalizedCoachException as e:
            logging.info(f"error while predicting duration: {e}")
            raise PersonalizedCoachException(e,sys)
        
class WorkoutModel:
    """
    Combined Workout Model wrapper to predict both workout and duration of workout,
    and save/load as a single .pkl/joblib file 
    """
    
    def __init__(self, workout_model, duration_model):
        self.workout_model = workout_model
        self.duration_model = duration_model
        
    def predict(self, user_data):
        workout = self.workout_model.predict(user_data)
        duration = self.duration_model.predict(user_data)
        results = []
        for i in range(len(user_data)):
            results.append({
                "workout":workout[i],
                "duration":duration[i]
            })
        return results

    def save(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)
        logging.info(f"Combined WorkoutModel saved at:{filepath}")
    
    @classmethod
    def load(cls, filepath):
        logging.info(f"Loading Workout Model from: {filepath}")
        return joblib.load(filepath)