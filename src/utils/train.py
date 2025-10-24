from src.custom_logging.logger import logging
from src.exception.exception import PersonalizedCoachException
from src.etl.etl_pipeline import ETLPipeline
from src.pipeline.training_pipeline import TrainingPipeline
import os,sys
from dotenv import load_dotenv
load_dotenv()

class Trainer:
    def __init__(self):
        self.etl=ETLPipeline()
        self.training=TrainingPipeline()
        
    def initiate_trainer(self):
        try:
            self.etl.run_etl()
            self.training.initiate_training()
        except PersonalizedCoachException as e:
            raise PersonalizedCoachException(e,sys)
if __name__=="__main__":
    train=Trainer().initiate_trainer()
    print(train)