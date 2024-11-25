from . import country_name_mapping

def transform_country_names(row):
    if row["Entity"] in country_name_mapping:
        row["Entity"] = country_name_mapping[row["Entity"]]
    return row