import json 

with open("ETLPipeline/transform/country_name_mapping.json", "r") as file:
    country_name_mapping = json.load(file)