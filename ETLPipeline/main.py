import sys
import pandas as pd
from extract.get_data_from_kaggle import download_crime_dataset, download_mental_health_dataset
from extract.get_data_from_file import get_gapminder_data_from_file
from transform.transform_crime_mental_health_dataframes import transform_crime_mental_health_dataframes
from transform.transform_gapminder import transform_gapminder
from load.mysql import load_dataframe_to_mysql

# Extract (download) crime and mental health data from Kaggle API
crime_dataset_path = download_crime_dataset() + "/crime-trends-and-operations-of-criminal-justice-systems-un-cts-csv-1.csv"
mental_health_dataset_path = download_mental_health_dataset() + "/Mental health Depression disorder Data.csv"
# Extract (from file) gapminder data
gapminder_df = get_gapminder_data_from_file()

# Put csv files into pandas dataframes
crime_df = pd.read_csv(crime_dataset_path)
mental_health_df = pd.read_csv(mental_health_dataset_path, index_col=0, low_memory=False)


# Transform crime and mental health data
combined, entities, country_to_years = transform_crime_mental_health_dataframes(crime_df, mental_health_df)

# Transform gapminder data
gapminder_df = transform_gapminder(gapminder_df, entities, country_to_years)

# Load mental health crime db
# Set database and table names
database = "DS2002FinalData"
mental_health_crime_table = "MentalHealthAndSACrimeRate"
gapminder_table = "Gapminder"
try:
    load_dataframe_to_mysql(combined, mental_health_crime_table, database)
    load_dataframe_to_mysql(gapminder_df, gapminder_table, database)
except Exception as e:
    print(f"failed to create database: {e}")
    sys.exit()

print("Done!")