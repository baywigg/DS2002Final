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

gcp_password = os.getenv("GCP_PASS")
gcp_host = os.getenv("GCP_IP")

def get_dataframe_from_mysql(table, database, local=True):
    return pd.read_sql(sql=f"SELECT * FROM {table}", con=create_connection(database, local))

def create_connection(database, local):
    return create_engine(f"mysql+pymysql://{user}:{quote(password)}@{host}/{database}") if local else create_engine(f"mysql+mysqlconnector://{user}:{gcp_password}@{gcp_host}/{database}")
