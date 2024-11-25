import pandas as pd

def transform_gapminder(gapminder, entities, country_to_years):
    # Drop unneeded column 'rownames'
    gapminder = gapminder.drop(columns=['rownames'])
    # Remove countries that only appear in gapminder, and not our other dataset
    gapminder = gapminder[gapminder["country"].isin(entities)]

    # Filter out country years that are not present in our other dataset
    gapminder = gapminder[gapminder.apply(lambda row: row["year"] in country_to_years.get(row["country"], set()), axis=1)].reset_index(drop=True)

    return gapminder