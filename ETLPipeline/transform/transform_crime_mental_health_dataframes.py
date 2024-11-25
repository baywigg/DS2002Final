import pandas as pd
from .transform_functions import transform_country_names

def transform_crime_mental_health_dataframes(crime_df, mental_health_df):
    # Remove second dataset that is a part of the mental health disorders one
    new_dataset_index = mental_health_df[mental_health_df['Entity'] == 'Entity'].index[0]
    mental_health_df = mental_health_df.loc[:new_dataset_index - 1]

    # Remove unneeded columns
    crime_df, mental_health_df = remove_columns(crime_df, mental_health_df)

    # Rename crime's columns to ensure they match mental health dataset
    crime_df.rename(columns={"country/territory": "Entity", "date":"Year", "rate": "Sexual Violence Rate"}, inplace=True)

    # Update the names of the territories to ensure both datasets share the same country names
    crime_df = crime_df.apply(transform_country_names, axis=1)


    # Concatenate the 'England' and 'Wales' rows into a new one
    # Get averaged values for each year
    filtered = mental_health_df[mental_health_df['Entity'].isin(['England', 'Wales'])]
    filtered = filtered.groupby('Year').mean(numeric_only=True).reset_index()
    # Drop original England and Wales rows
    mental_health_df = mental_health_df[~mental_health_df['Entity'].isin(['England', 'Wales'])]

    # Append the filtered DF to the mental health one 
    filtered["Entity"] = "United Kingdom (England and Wales)"
    mental_health_df = pd.concat([mental_health_df, filtered]).reset_index(drop=True)

    # Combine our crime and mental health datasets on Entity and year to exclude all the data not present in both
    crime_df = crime_df.dropna()
    combined =  pd.merge(mental_health_df, crime_df, on=["Entity", "Year"])
    # Get set of countries that are in the combined dataset
    entities = set(combined["Entity"].unique())
    # Get country to year mapping to use with gapminder dataset
    country_to_years = get_countries_to_years(combined)
    return combined, entities, country_to_years

def remove_columns(crime_df, mental_health_df):
    # Remove unneeded columns, and coerce other columns to ensure numeric
    mhd_columns_to_remove = ["Code", "Bipolar disorder (%)", "Eating disorders (%)"]
    mental_health_df = mental_health_df.drop(columns=mhd_columns_to_remove)

    crime_df = crime_df.drop(columns=["sexual violence"])

    mhd_numeric_columns = ["Year", "Schizophrenia (%)", "Anxiety disorders (%)", "Drug use disorders (%)", "Depression (%)", "Alcohol use disorders (%)"]
    crime_numeric_columns = ["date", "rate"]

    # Convert mental health columns to numeric
    for col in mhd_numeric_columns:
        mental_health_df[col] = pd.to_numeric(mental_health_df[col], errors="coerce")


    # Convert crime to numeric
    for col in crime_numeric_columns:
        crime_df[col] = pd.to_numeric(crime_df[col], errors="coerce")

    return crime_df, mental_health_df

def get_countries_to_years(df):
    # Create defaultdict of type set to store Entity : Years
    from collections import defaultdict
    c = defaultdict(set)
    for _, row in df.iterrows():
        c[row["Entity"]].add(row["Year"])
    return c