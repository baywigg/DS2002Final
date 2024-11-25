import csv
import pandas as pd

def get_gapminder_data_from_file():
    return pd.read_csv("ETLPipeline/data/gapminder.csv")
