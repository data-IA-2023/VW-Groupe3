import openmeteo_requests
from utilities import city_to_coordinates
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import *
from nlp import enregistrement_nlp


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def obtenir_meteo(latitude,longitude,date):
            
		# Make sure all required weather variables are listed here
		# The order of variables in hourly or daily is important to assign them correctly below
		url = "https://api.open-meteo.com/v1/meteofrance"
		date=date
		params = {
			"latitude": latitude,
			"longitude": longitude,
			"daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_hours"],
			"timezone": "auto"
		}
		responses = openmeteo.weather_api(url, params=params)

		# Process first location. Add a for-loop for multiple locations or weather models
		response = responses[0]
		print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
		print(f"Elevation {response.Elevation()} m asl")
		print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
		print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

		# Process daily data. The order of variables needs to be the same as requested.
		daily = response.Daily()
		daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
		daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
		daily_precipitation_hours = daily.Variables(2).ValuesAsNumpy()

		daily_data = {"date": pd.date_range(
			start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
			end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = daily.Interval()),
			inclusive = "left"
		)}
		daily_data["temperature_2m_max"] = daily_temperature_2m_max
		daily_data["temperature_2m_min"] = daily_temperature_2m_min
		daily_data["precipitation_hours"] = daily_precipitation_hours
		daily_dataframe = pd.DataFrame(data = daily_data)
		return daily_dataframe


def df_to_date(Date, df):
    if Date == "aujourdhui":
        id = 1
        Date = date.today()
    elif Date == "demain":
        id = 2
        Date = date.today() + timedelta(days=1)
    elif Date == "après demain":
        id = 3
        Date = date.today() + timedelta(days=2)
    print(df)
    return {"df":df.at[id, "precipitation_hours"],"date":Date,"temperaturemin":df.at[id, "temperature_2m_min"],"temperaturemax":df.at[id, "temperature_2m_max"]}

def convertisseur_meteo(id):
		if id == 0.0:
			return "Il fait beau"
		elif  0<id<5:
			return "Un peu de pluie"
		else:
			return "Beaucoup de pluie"




         