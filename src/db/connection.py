from src.custom_logging.logger import logging
from src.exception.exception import PersonalizedCoachException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
from dotenv import load_dotenv
load_dotenv()

def get_engine(db_url: str=None):
    try:
        db_uri = os.getenv("DB_URI")
        if not db_uri:
            raise ValueError("DB_URI environment variable not set")
        engine = create_engine(db_uri)
        return engine
    except Exception as e:
        logging.error(f"Error occurred while getting database engine: {e}")
        raise PersonalizedCoachException(e, sys)
