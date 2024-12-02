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

def load_dataframe_to_gcp(df, table_name, database):
    try:
        # Create connection string
        con_str = f"mysql+mysqlconnector://{user}:{gcp_password}@{gcp_host}/{database}"
        engine = create_engine(con_str)
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    except Exception as e:
        raise RuntimeError(f"Error loading dataframe to GCP: {e}")

def load_dataframe_to_mysql(df, table_name, database):
    try:
        # Create database and connection
        create_database(database)
    except Exception as e:
        raise RuntimeError(f"Error creating database: {e}")
    
    try:
        engine = create_connection(database)
        # Load into MySQL DB
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    except Exception as e:
        raise RuntimeError(f"Error loading dataframe to MySQL: {e}")

def create_database(database):
    try:
        connection = pymysql.connect(host=host, user="root", password=password)
    except Exception as e:
        raise RuntimeError(f"Error creating connection to MySQL server: {e}")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
    except Exception as e:
        raise RuntimeError(f"Error executing database creation query: {e}")
    finally:
        connection.close()

def create_connection(database):
    try:
        connection = create_engine(f"mysql+pymysql://{user}:{quote(password)}@{host}/{database}")
        return connection
    except Exception as e:
        raise RuntimeError(f"Error creating connection to MySQL database: {e}")
