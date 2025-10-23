import pandas as pd
import sys
from sqlalchemy.engine import Engine
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import NoSuchTableError

from src.custom_logging.logger import logging
from src.exception.exception import PersonalizedCoachException

class Extractor:
    def __init__(self, db_engine:Engine=None):
        """
        db_session: SQLAlchemy session for DB access
        """
        try:
            
            self.db_engine=db_engine
            
        except PersonalizedCoachException as e:
            logging.info(f"Provide the session")
            raise PersonalizedCoachException(e,sys)
        
    def from_db(self, table: str = None, query: str = None) -> pd.DataFrame:
        """
        Load Data from the database into a DataFrame.
        Either provide a 'table' name or a custom SQL 'query'.
        """
        engine = self.db_engine
        try:
            if query: # create SQL query
                return pd.read_sql(query, con=engine)
            elif table: # full table load
                return pd.read_sql_table(table, con=engine)
            else:
                raise ValueError("Either 'table' or 'query' must be provided.")
        except PersonalizedCoachException as e:
            logging.error(f"Error in from_db(): {e}")
            raise PersonalizedCoachException(e,sys)
        
        