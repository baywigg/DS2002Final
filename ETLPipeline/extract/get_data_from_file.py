import csv
import pandas as pd

def get_gapminder_data_from_file():
    try:
        return pd.read_csv("ETLPipeline/data/gapminder.csv")
    except Exception as e:
        raise RuntimeError(f"Error reading Gapminder data from file: {e}")
