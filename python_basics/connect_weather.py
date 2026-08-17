import requests
from dotenv import load_dotenv
import os 

# LOAD THE ENVIRONMENT VARIABLES FROM .ENV
load_dotenv()

# DECLARING THE VARIABLES
OPENWEATHERMAP_APIKEY = os.getenv("OPENWEATHERMAP_APIKEY")
OPENWEATHERMAP_ZIPCODE = input("Enter your zip code: ")
OPENWEATHERMAP_COUNTRYCODE = input("Enter your country code: ")

# FORMING THE URL
OPENWEATHERMAP_URL = f"https://api.openweathermap.org/data/2.5/weather?zip={OPENWEATHERMAP_ZIPCODE},{OPENWEATHERMAP_COUNTRYCODE}&appid={OPENWEATHERMAP_APIKEY}"

# CONNECTING TO URL
response = requests.get(OPENWEATHERMAP_URL)

# PRINT URL STATUS CODE
print(response.status_code)

# PRINT URL RESPONSE
print(response.json())