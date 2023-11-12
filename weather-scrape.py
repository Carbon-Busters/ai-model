import requests
import csv
import time

'''
station_data
    "\ufeffStationID": string
    "Location": string (city, state, country)
    "Data Source": string
    "Data Years": string
    "Ground Surface": string
    "Overall Albedo": string
    "Lat": string
    "Long": string

station list
    [station_data]
'''

# Compile albedo data from csv file
station_list = []
ALBEDO_DATA_CSV = "albedo.csv"

# Open the CSV file for reading
with open(ALBEDO_DATA_CSV, 'r', newline='', encoding='utf-8') as csvfile:
    # Create a CSV DictReader object
    csv_reader = csv.DictReader(csvfile)
    # Read and print each row of the CSV file
    for row in csv_reader:
        station_list.append(row)

# Iterate through stations and get weather data
for station in station_list:
    lat = station["Lat"]
    long = station["Long"]
    API_URL = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={long}&start_date=2022-01-01&end_date=2022-12-31&hourly=temperature_2m,relative_humidity_2m,rain,snowfall,cloud_cover,wind_speed_10m&timezone=America%2FNew_York"
    
    # Make a GET request to the API
    response = requests.get(API_URL)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and return the JSON data
        data = response.json()
        data_to_csv = {
            "Timestamp": data["hourly"]["time"],
            "Temperature (deg C)": data["hourly"]["temperature_2m"],
            "Relative Humidity (%)": data["hourly"]["relative_humidity_2m"],
            "Wind Speed (km/h)": data["hourly"]["wind_speed_10m"],
            "Rain (mm)": data["hourly"]["rain"],
            "Snowfall (cm)": data["hourly"]["snowfall"],
            "Cloud Cover (%)": data["hourly"]["cloud_cover"],
        }
        # Open the CSV file for writing
        with open("weather-data/" + station["\ufeffStationID"] + ".csv", 'w', newline='', encoding='utf-8') as csvfile:
            # Extract the keys (column names) from the dictionary
            fieldnames = list(data_to_csv.keys())
            # Create a CSV writer object
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the header to the CSV file
            csv_writer.writeheader()
            # Determine the maximum length of the lists to iterate over
            max_length = max(len(v) for v in data_to_csv.values())
            # Write each row of the dictionary to the CSV file
            for i in range(max_length):
                row_data = {key: data_to_csv[key][i] if i < len(data_to_csv[key]) else '' for key in fieldnames}
                csv_writer.writerow(row_data)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        #return None

    time.sleep(5.0)