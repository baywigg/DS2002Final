from sqlalchemy import create_engine
from urllib.parse import quote
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")

def load_dataframe_to_mysql(df, table_name, database):
    # Create database and connection
    try:
        create_database(database)
    except Exception as e:
        raise
    engine = create_connection(database)
    # Load into mySQL DB
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)


def create_database(database):
    try:
        connection = pymysql.connect(host=host, user="root", password=password)
    except Exception as e:
        raise
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
    finally:
        connection.close()
    

def create_connection(database):
    connection = create_engine(f"mysql+pymysql://{user}:{quote(password)}@{host}/{database}")
    return connection
    