from src.custom_logging.logger import logging
from src.exception.exception import PersonalizedCoachException
from src.etl.extract import Extractor
from src.etl.transform import Transformer
from src.etl.load import Loader
from src.db.connection import get_engine
from src.contants import (NUTRITION_TABLE_NAME,FAQ_TABLE_NAME,WORKOUTS_TABLE_NAME)
import os
import sys
import pandas as pd

## creating engine as global 
ENGINE = get_engine()

class ETLPipeline:
    def __init__(self):
        self.extractor = Extractor(ENGINE)
        self.transformer = Transformer()
        self.loader = Loader()
    
    def run_etl(self):
        try:
            logging.info("ETL Pipeline initiated.")
            # nutrition data
            nutrition_df = self.extractor.from_db(table=NUTRITION_TABLE_NAME)
            transformed_nutrition_df = self.transformer.transform_nutrition(nutrition_df)
            self.loader.save_csv(df=pd.DataFrame(transformed_nutrition_df), path="data/processed/Nutrition_transformed.csv") # save the clean data in csv format in desired path
            
            # workout data
            workout_df = self.extractor.from_db(table=WORKOUTS_TABLE_NAME)
            transformed_workout_df = self.transformer.transform_workout(workout_df)
            self.loader.save_csv(df=pd.DataFrame(transformed_workout_df), path="data/processed/Workout_tranformed.csv")
            
            # FAQ data
            faq_df = self.extractor.from_db(table=FAQ_TABLE_NAME)
            transformed_faq_df = self.transformer.transform_faq(faq_df)
            self.loader.save_csv(df=pd.DataFrame(transformed_faq_df), path="data/processed/FAQ_transformed.csv")
            
            logging.info("ETL Pipeline finished.")
            
            print("ETL completed for all datasets.")
            
        except PersonalizedCoachException as e:
            logging.error(f"Error occured while running etl_pipeline: {e}")
            raise PersonalizedCoachException(e,sys)
