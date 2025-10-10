from src.logging.logger import logging
from src.exception.exception import PersonalizedCoachException
import os
import sys
import pandas as pd

class Loader:
    def save_csv(self, df, path):
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            df.to_csv(path, index=False)
            print(f"Saved processed data to file path {path}")
        except PersonalizedCoachException as e:
            logging.info(f"Error occured in saving the transformed data: {e}")
            raise PersonalizedCoachException(e,sys)