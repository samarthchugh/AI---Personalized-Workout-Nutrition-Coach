from src.custom_logging.logger import logging
from src.exception.exception import PersonalizedCoachException
from src.db.connection import get_engine
from src.db.models import base, Workout, Nutrition, FAQ
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
import pandas as pd
import os
import sys

class DataBaseSeeder:
    """
    Send CSV data into PostgreSQL database via ORM
    """
    def __init__(self, db_url: str=None):
        try:
            self.engine = get_engine(db_url)
            base.metadata.create_all(self.engine)
            self.session = sessionmaker(bind=self.engine)
            
        except Exception as e:
            logging.error(f"Error occurred while initializing database seeder: {e}")
            raise PersonalizedCoachException(e, sys)
        
    def seed_csvs(self, csv_path: str, table_type: str):
        try:
            df = pd.read_csv(csv_path)
            session = self.session()
            model_map = {
                "Workout": Workout,
                "Nutrition": Nutrition,
                "FAQ": FAQ
            }
            if table_type not in model_map:
                raise ValueError(f"Invalid table type: {table_type}")
            
            ModelClass = model_map[table_type]
            records_added = 0
            for _, row in df.iterrows():
                try:
                    obj = ModelClass(**row.to_dict())
                    session.add(obj)
                    records_added += 1
                except IntegrityError as ie:
                    logging.warning(f"Skipping duplicate record: {ie}")
                    session.rollback()
                except Exception as e:
                    session.rollback()
                    logging.error(f"Error adding record: {e}")
            session.commit()
            session.close()
            logging.info(f"Seeded {records_added} rows into {table_type} table from {csv_path}")
            self.reset_sequence(ModelClass.__tablename__)
            logging.info("Workouts data seeded successfully.")
        except IntegrityError as ie:
            logging.error(f"Integrity error while seeding workouts: {ie}")
            raise PersonalizedCoachException(ie, sys)
        except Exception as e:
            logging.error(f"Error occurred while seeding workouts: {e}")
            raise PersonalizedCoachException(e, sys)
        
    def reset_sequence(self, table_name:str):
        """Ensure PostgreSQL autoincrement sequences match max(id) after bulk insert"""
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text(
                        f"""
                    SELECT setval(
                        pg_get_serial_sequence('"{table_name}"', 'id'),
                        COALESCE((SELECT MAX(id) FROM "{table_name}"), 1),
                        TRUE
                    );
                    """
                    )
                )
                conn.commit()
                logging.info(f"🔄 Sequence reset for table: {table_name}")
        except PersonalizedCoachException as e:
            logging.error(f"Error resetting sequence for {table_name}: {e}")
            raise PersonalizedCoachException(e, sys)
        
if __name__ == "__main__":
    seeder = DataBaseSeeder()
    seeder.seed_csvs(csv_path=os.path.join("data", "raw_data", "workouts.csv"), table_type="Workout")
    seeder.seed_csvs(csv_path=os.path.join("data", "raw_data", "nutrition.csv"), table_type="Nutrition")
    seeder.seed_csvs(csv_path=os.path.join("data", "raw_data", "faq.csv"), table_type="FAQ")