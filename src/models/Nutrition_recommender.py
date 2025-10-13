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
from sklearn.multioutput import MultiOutputRegressor

class NutritionRecommender:
    """
    Nutrition model wrapper:
    - meal_pipeline: classifier that predicts meal_name(LabelEncoded externally)
    - nutrients_pipeline: multi-output regressor predicting calories, protein_g, carbs_g, fats_g
    Both pipelines include a ColumnTransformer with numeric imputer + scaler and categorical OHE.
    """

    def __init__(self,categorial_features=None, numerical_features=None, random_state=42):
        self.categorical_features = categorial_features or ['gender', 'goal', 'diet_type']
        self.numerical_features = numerical_features or ['age', 'bmi']
        self.random_state = random_state
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore',sparse_output=False),self.categorical_features),
                ('num',Pipeline(steps=[
                    ('imputer', KNNImputer(n_neighbors=5)),
                    ('scaler', StandardScaler())
                ]),self.numerical_features)
            ], remainder='drop',
            verbose_feature_names_out=False
        )
        
        self.meal_pipeline = Pipeline(
            steps=[
                ('preprocessor',preprocessor),
                ('classifier', RandomForestClassifier(n_estimators=200, random_state=self.random_state))
            ]
        )
        
        self.nutrients_pipeline = Pipeline(
            steps=[
                ('preprocessor', preprocessor),
                ('regressor', MultiOutputRegressor(RandomForestRegressor(n_estimators=200, random_state=self.random_state)))
            ]
        )
        
    def fit(self, X, y_meal, y_nutrients):
        try:
            self.meal_pipeline.fit(X, y_meal)
            self.nutrients_pipeline.fit(X, y_nutrients)
        except PersonalizedCoachException as e:
            logging.info(f"error while fitting the data: {e}")
            raise PersonalizedCoachException(e,sys)
        
    def predict_meal(self, X):
        try:
            return self.meal_pipeline.predict(X)
        except PersonalizedCoachException as e:
            logging.info(f"Error while predicting meal: {e}")
            raise PersonalizedCoachException(e,sys)
    
    def predict_nutrients(self,X):
        try:
            return self.nutrients_pipeline.predict(X)
        except PersonalizedCoachException as e:
            logging.info(f"Error while predicting Nutrients: {e}")
        
class NutrientModel:
    """
    Combined model wrapper to predict both meal and nutrients value,
    and save/load as a single .pkl/.joblib file
    """
    def __init__(self, meal_model, nutrients_model):
        self.meal_model = meal_model
        self.nutrients_model = nutrients_model
        
    def predict(self, user_data):
        meal_preds = self.meal_model.predict(user_data)
        nutrients_pred = self.nutrients_model.predict(user_data)
        
        results = []
        for i in range(len(user_data)):
            results.append({
                "meal":meal_preds[i],
                "calories":nutrients_pred[i][0],
                "protein_g":nutrients_pred[i][1],
                "fats_g":nutrients_pred[i][2],
                "carbs_g":nutrients_pred[i][3]
            })
        return results
    
    def save(self, filepath):
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        joblib.dump(self, filepath)
        logging.info(f"💾 Combined NutritionModel saved at: {filepath}")
        
    @classmethod
    def load(cls, filepath):
        logging.info(f"📦 Loading NutritionModel from: {filepath}")
        return joblib.load(filepath)