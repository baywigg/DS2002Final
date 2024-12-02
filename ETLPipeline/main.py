import sys
import pandas as pd
from extract.get_data_from_kaggle import download_crime_dataset, download_mental_health_dataset
from extract.get_data_from_file import get_gapminder_data_from_file
from transform.transform_crime_mental_health_dataframes import transform_crime_mental_health_dataframes
from transform.transform_gapminder import transform_gapminder
from load.mysql import load_dataframe_to_mysql, load_dataframe_to_gcp

try:
    # Extract (download) crime and mental health data from Kaggle API
    crime_dataset_path = download_crime_dataset() + "/crime-trends-and-operations-of-criminal-justice-systems-un-cts-csv-1.csv"
    mental_health_dataset_path = download_mental_health_dataset() + "/Mental health Depression disorder Data.csv"
except Exception as e:
    print(f"Failed to download datasets from Kaggle: {e}")
    sys.exit()

try:
    # Extract (from file) gapminder data
    gapminder_df = get_gapminder_data_from_file()
except Exception as e:
    print(f"Failed to load Gapminder data from file: {e}")
    sys.exit()

try:
    # Put csv files into pandas dataframes
    crime_df = pd.read_csv(crime_dataset_path)
    mental_health_df = pd.read_csv(mental_health_dataset_path, index_col=0, low_memory=False)
except Exception as e:
    print(f"Failed to read dataset into pandas DataFrame: {e}")
    sys.exit()

try:
    # Transform crime and mental health data
    combined, entities, country_to_years = transform_crime_mental_health_dataframes(crime_df, mental_health_df)
except Exception as e:
    print(f"Failed to transform crime and mental health dataframes: {e}")
    sys.exit()

try:
    # Transform gapminder data
    gapminder_df = transform_gapminder(gapminder_df, entities, country_to_years)
except Exception as e:
    print(f"Failed to transform Gapminder data: {e}")
    sys.exit()

# Load mental health crime db
# Set database and table names
database = "DS2002FinalData"
mental_health_crime_table = "MentalHealthAndSACrimeRate"
gapminder_table = "Gapminder"

local = input("Would you like to save data in a local MySQL database? (y/n): ")
if local not in ["y", "n"]:
    print("Please input either 'y' or 'n'.")
    sys.exit()

if local == "y":
    try:
        load_dataframe_to_mysql(combined, mental_health_crime_table, database)
        load_dataframe_to_mysql(gapminder_df, gapminder_table, database)
    except Exception as e:
        print(f"Failed to create local database: {e}")
        sys.exit()

gcp = input("Would you like to save data in a GCP MySQL database? (y/n): ")
if gcp not in ["y", "n"]:
    print("Please input either 'y' or 'n'.")
    sys.exit()

if gcp == "y":
    try:
        load_dataframe_to_gcp(combined, mental_health_crime_table, database)
        load_dataframe_to_gcp(gapminder_df, gapminder_table, database)
    except Exception as e:
        print(f"Failed to upload to GCP: {e}")
        sys.exit()

print("Done!")
