import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")

def get_dataframe_from_mysql(table, database):
    return pd.read_sql(sql=f"SELECT * FROM {table}", con=create_connection(database))

def create_connection(database):
    return create_engine(f"mysql+pymysql://{user}:{quote(password)}@{host}/{database}")