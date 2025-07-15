#This is for create weather_data.json
import requests
import json
import os # For checking if the file exists and managing paths
print(f"Current working directory: {os.getcwd()}")
# --- Configuration ---
# REPLACE THIS WITH YOUR ACTUAL API KEY FROM WeatherAPI.com
WEATHER_API_KEY = "e1a375311c47438f941175631250907" 
# Example location (you can change this)
LOCATION = "Bangkok" # e.g., "London", "New York", "Tokyo"
# Name for your dummy JSON file
DUMMY_JSON_FILENAME = "weather_data.json"
# Get the directory where the current script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path for the dummy JSON file
DUMMY_JSON_FILEPATH = os.path.join(script_dir, DUMMY_JSON_FILENAME)

# WeatherAPI.com endpoint for current weather
API_URL = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={LOCATION}"

print(f"--- Fetching Weather Data for {LOCATION} ---")

try:
    # Make the GET request to the API
    response = requests.get(API_URL)

    # Check if the request was successful (status code 200)
    response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

    # Parse the JSON response
    weather_data = response.json()

    # --- Save the data to your dummy JSON file ---
    with open(DUMMY_JSON_FILEPATH, 'w', encoding='utf-8') as f:
        # Use json.dump for writing JSON to a file
        # indent=4 makes the JSON human-readable (pretty-printed)
        json.dump(weather_data, f, ensure_ascii=False, indent=4)

    print(f"Successfully fetched weather data for {LOCATION} and saved to '{DUMMY_JSON_FILENAME}'.")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err} (Status Code: {response.status_code})")
    if response.status_code == 401:
        print("Check your API key. It might be invalid or missing.")
    elif response.status_code == 403:
        print("Access forbidden. Ensure your plan covers this request or your key is activated.")
    elif response.status_code == 400:
        print("Bad request. Check your location parameter or API documentation.")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}. Check your internet connection.")
except requests.exceptions.Timeout as timeout_err:
    print(f"Request timed out: {timeout_err}. The API might be slow or your connection is unstable.")
except requests.exceptions.RequestException as req_err:
    print(f"An unexpected request error occurred: {req_err}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

