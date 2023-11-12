from typing import Union

import pandas as pd
from fastapi import FastAPI

from utils import *

app = FastAPI()

zip_lat_long_csv = pd.read_csv(
    "https://gist.githubusercontent.com/erichurst/7882666/raw/5bdc46db47d9515269ab12ed6fb2850377fd869e/US%2520Zip%2520Codes%2520from%25202013%2520Government%2520Data"
)
lat_long_mapping = dict()
for i, row in zip_lat_long_csv.iterrows():
    zipcode = str(int(row["ZIP"])).zfill(5)
    lat = str(row["LAT"])
    lng = str(row["LNG"])
    lat_long_mapping[zipcode] = (lat, lng)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/")
def read_input(zipcode: str = "00601", input: str = ""):
    # Get lat/long
    lat_long = lat_long_mapping[zipcode]
    snow_rain_data = list_of_day_snow_rain(str(lat_long[0]), str(lat_long[1]))
    api_output = get_similarity_environment_albedo(snow_rain_data, input)
    api_output["lat"] = lat_long[0]
    api_output["long"] = lat_long[1]
    print(api_output)
    return api_output
