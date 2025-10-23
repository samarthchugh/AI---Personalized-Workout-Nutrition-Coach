from src.exception.exception import PersonalizedCoachException
from src.custom_logging.logger import logging

import pandas as pd
import numpy as np
import sys
import re

class Transformer:
    def __init__(self):
        pass
    
    def clean_text(self, text:str):
        try:
            """LowerCase, remove extra spaces, and strip unwanted symbols."""
            if pd.isnull(text):
                return text
            text = text.lower() # lowercase
            text = re.sub(r'[^a-z0-9\s]','',text) # remove symbols, keep alphanum + space
            text = re.sub(r'\s+',' ',text).strip() # remove extra spaces
            return text
        except PersonalizedCoachException as e:
            logging.error(f"Error occured in clean_text: {e}")
            raise PersonalizedCoachException(e,sys)

    def drop_id(self,df:pd.DataFrame) ->pd.DataFrame:
        try:
            """DROP ID column if it exists (case-insensitive)."""
            for col in df.columns:
                if col.lower()=="id":
                    df=df.drop(columns=[col])
            return df
        except PersonalizedCoachException as e:
            logging.error(f"Error occured in drop_id: {e}")
            raise PersonalizedCoachException(e,sys)    
        
    def transform_nutrition(self,df:pd.DataFrame)->pd.DataFrame:
        try:
            df=self.drop_id(df)
            """only clean input features (not targets)"""
            feature_cols=['gender','goal','diet_type']
            for col in feature_cols:
                if col in df.columns:
                    df[col]=df[col].astype(str).apply(self.clean_text)
                    
            return df
        except PersonalizedCoachException as e:
            logging.error(f"Error occured in transform_nutrition: {e}")
            raise PersonalizedCoachException(e,sys)
    
    def transform_workout(self,df:pd.DataFrame) -> pd.DataFrame:
        try:
            df = self.drop_id(df)
            """only clean input features"""
            feature_cols=['intensity','muscle_group','gender','goal','fitness_level']
            for col in feature_cols:
                if col in df.columns:
                    df[col]=df[col].astype(str).apply(self.clean_text)
                    
            return df
        except PersonalizedCoachException as e:
            logging.error(f"Error occured in transform_workout: {e}")
            raise PersonalizedCoachException(e,sys)
    
    def transform_faq(self,df:pd.DataFrame) -> pd.DataFrame:
        try:
            df = self.drop_id(df)
            return df
        except PersonalizedCoachException as e:
            logging.error(f"Error occured in transform_faq: {e}")
            raise PersonalizedCoachException(e,sys)