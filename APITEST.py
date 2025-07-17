import numpy as np
import requests
import json
import os
import matplotlib.pyplot as plt

# --- Configuration ---
DEFAULT_NUMERIC_VALUE = 0
DUMMY_JSON_FILENAME = "weather_data.json" # Name for your dummy JSON file
script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory where the current script is located
DUMMY_JSON_FILEPATH = os.path.join(script_dir, DUMMY_JSON_FILENAME) # Construct the full path for the dummy JSON file

# --- Main Application Logic ---
API_KEY = ""
City = ""
API_data = None

# --- Loop for API Key Validation ---
while True:
    API_KEY = input("Enter your OpenWeatherMap API Key: ").strip()
    if not API_KEY:
        print("API Key cannot be empty. Please try again.")
        continue

    TEST_API_KEY_URL = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={API_KEY}"
    print("\n--- Validating API Key ---")
    try:
        test_response = requests.get(TEST_API_KEY_URL, timeout=5)
        test_response.raise_for_status()

        print("API Key seems valid.")
        break

    except requests.exceptions.HTTPError as http_err:
        if test_response.status_code == 401:
            print("Error: Invalid API Key. Please double-check your OpenWeatherMap API key.")
        else:
            print(f"An HTTP error occurred during API Key validation: {http_err} (Status Code: {test_response.status_code})")
        print("Please re-enter your API Key.")
        continue

    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred during API Key validation: {conn_err}. Please check your internet connection.")
        print("Please re-enter your API Key.")
        continue

    except requests.exceptions.Timeout as timeout_err:
        print(f"Request timed out during API Key validation: {timeout_err}. The API might be slow or your connection is unstable.")
        print("Please re-enter your API Key.")
        continue

    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected request error occurred during API Key validation: {req_err}")
        print("Please re-enter your API Key.")
        continue

    except Exception as e:
        print(f"An unexpected error occurred during API Key validation: {e}")
        print("Please re-enter your API Key.")
        continue

# --- Loop for City Validation and Data Fetch ---
while True:
    City = input("Enter the city name for weather forecast (e.g., Bangkok, London): ").strip()
    if not City:
        print("City name cannot be empty. Please try again.")
        continue

    URL = f'https://api.openweathermap.org/data/2.5/forecast?q={City}&appid={API_KEY}'

    print(f"\n--- Attempting to Fetch Weather Data for {City} ---")

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        API_data = response.json()

        if 'list' not in API_data:
            print(f"Error: No forecast data found for {City}. Response: {API_data.get('message', 'Unknown error')}")
            API_data = None
            print("Please re-enter the city name.")
            continue

        print(f"Successfully fetched weather data for {City}.")
        break

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Error: City '{City}' not found. Please check the spelling.")
        elif response.status_code == 401:
            print("Error: API Key became invalid during city fetch. Please re-enter API Key and City.")
            continue
        else:
            print(f"An HTTP error occurred during data fetch: {http_err} (Status Code: {response.status_code})")
            print("An API-specific error occurred. Please try a different city or check your internet.")
        print("Please re-enter the city name.")
        continue

    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred during data fetch: {conn_err}. Please check your internet connection.")
        print("Please re-enter the city name.")
        continue

    except requests.exceptions.Timeout as timeout_err:
        print(f"Request timed out during data fetch: {timeout_err}. The API might be slow or your connection is unstable.")
        print("Please re-enter the city name.")
        continue

    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected request error occurred during data fetch: {req_err}")
        print("Please re-enter the city name.")
        continue

    except json.JSONDecodeError:
        print("Error: Could not decode JSON response from API. Response might not be valid JSON.")
        print("Please re-enter the city name.")
        continue

    except Exception as e:
        print(f"An unexpected error occurred during data fetch: {e}")
        print("Please re-enter the city name.")
        continue

cleaned_data_list = []

def is_numeric(value):
    try:
        int(value)
        return True
    except ValueError:
        try:
            float(value)
            return True
        except ValueError:
            return False

time = [(item['dt_txt']) for item in API_data['list']]
temp = [round(item['main']['temp'] - 273.15, 2) for item in API_data['list']]

cleaning_list = temp

print("\n--- Cleaning Data from List ---")
for item in cleaning_list:
    item_str = str(item).strip()
    if is_numeric(item_str):
        cleaned_value = float(item_str)
    else:
        cleaned_value = DEFAULT_NUMERIC_VALUE
        print(f"  Replaced non-numeric '{item_str}' with {DEFAULT_NUMERIC_VALUE}.")
    cleaned_data_list.append(cleaned_value)

if cleaned_data_list:
    cleaned_np_array = np.array(cleaned_data_list)
    print(f"\n--- Cleaned Data as NumPy Array (Shape: {cleaned_np_array.shape}) ---")
    print(cleaned_np_array)

    print("\n--- Basic Statistical Analysis ---")
    print(f"Mean Temperature: {np.mean(cleaned_np_array):.2f}°C")
    print(f"Median Temperature: {np.median(cleaned_np_array):.2f}°C")
    print(f"Sum of Temperatures: {np.sum(cleaned_np_array):.2f}°C")
    print(f"Minimum Temperature: {np.min(cleaned_np_array):.2f}°C")
    print(f"Maximum Temperature: {np.max(cleaned_np_array):.2f}°C")
    print(f"Standard Deviation of Temperatures: {np.std(cleaned_np_array):.2f}°C")

    # --- Plotting the Temperature Data ---
    print(f"\n--- Generating Temperature Forecast Plot for {City} ---")
    plt.figure(figsize=(12, 6))
    plt.plot(time, temp, marker='o', linestyle='-', markersize=4, color='skyblue')
    
    plt.title(f'Temperature Forecast for {City}')
    plt.xlabel('Date and Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    plt.show()

else:
    print("No valid numerical data was cleaned or processed for plotting.")

print(f"\nTemperature forecast in {City}:")
if time and temp and len(time) == len(temp):
    for t, tp in zip(time, temp):
        print(f"{t}: {tp}°C")
else:
    print("Could not display detailed forecast due to missing or inconsistent data.")

# --- Corrected: Prepare structured data for JSON saving ---
# Create a list of dictionaries, where each dictionary represents a forecast entry
structured_weather_data = []
if time and temp and len(time) == len(temp):
    for t, tp in zip(time, temp):
        structured_weather_data.append({
            "time": t,
            "temperature_c": tp
        })
    
    # Add city information to the top level of the JSON for context
    final_json_data = {
        "city": City,
        "forecast_data": structured_weather_data
    }

    # --- Save the structured data to your dummy JSON file ---
    try:
        with open(DUMMY_JSON_FILEPATH, 'w', encoding='utf-8') as f:
            json.dump(final_json_data, f, ensure_ascii=False, indent=4)
        print(f"\nSuccessfully saved structured weather data to '{DUMMY_JSON_FILEPATH}'.")
    except Exception as e:
        print(f"\nError saving JSON data to file: {e}")
else:
    print("\nSkipping JSON save: No complete time and temperature data to save.")

