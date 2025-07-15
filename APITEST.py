import numpy as np
import requests
import json # Import json for JSONDecodeError handling
import os # not used 

# --- Configuration ---
# Default value to replace non-numeric entries during cleaning
DEFAULT_NUMERIC_VALUE = 0

# --- Main Application Logic ---
API_KEY = "" # Initialize API_KEY
City = ""    # Initialize City
API_data = None # Initialize API_data to None

# --- Loop for API Key Validation ---
while True:
    API_KEY = input("Enter your OpenWeatherMap API Key: ").strip()
    if not API_KEY:
        print("API Key cannot be empty. Please try again.")
        continue # Restart the loop to ask for API Key again

    # Test API Key with a known, simple request (e.g., current weather for London)
    # This helps isolate API key issues before trying a full forecast.
    TEST_API_KEY_URL = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={API_KEY}"
    print("\n--- Validating API Key ---")
    try:
        test_response = requests.get(TEST_API_KEY_URL, timeout=5) # Add a timeout for safety
        test_response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        # If we reach here, the API key is likely valid (or at least not 401/404 for a basic call)
        print("API Key seems valid.")
        break # Exit API key loop as the key is validated

    except requests.exceptions.HTTPError as http_err:
        if test_response.status_code == 401:
            print("Error: Invalid API Key. Please double-check your OpenWeatherMap API key.")
        else:
            # Catch other HTTP errors during key validation (e.g., 500 server error)
            print(f"An HTTP error occurred during API Key validation: {http_err} (Status Code: {test_response.status_code})")
        print("Please re-enter your API Key.")
        continue # Restart API key loop

    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred during API Key validation: {conn_err}. Please check your internet connection.")
        print("Please re-enter your API Key.")
        continue # Restart API key loop

    except requests.exceptions.Timeout as timeout_err:
        print(f"Request timed out during API Key validation: {timeout_err}. The API might be slow or your connection is unstable.")
        print("Please re-enter your API Key.")
        continue # Restart API key loop

    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected request error occurred during API Key validation: {req_err}")
        print("Please re-enter your API Key.")
        continue # Restart API key loop

    except Exception as e:
        print(f"An unexpected error occurred during API Key validation: {e}")
        print("Please re-enter your API Key.")
        continue # Restart API key loop


# --- Loop for City Validation and Data Fetch ---
while True:
    City = input("Enter the city name for weather forecast (e.g., Bangkok, London): ").strip()
    if not City:
        print("City name cannot be empty. Please try again.")
        continue # Restart the loop to ask for city name again

    # OpenWeatherMap API endpoint for 5-day / 3-hour forecast
    # Units are default Kelvin, so we'll convert to Celsius
    URL = f'https://api.openweathermap.org/data/2.5/forecast?q={City}&appid={API_KEY}'

    print(f"\n--- Attempting to Fetch Weather Data for {City} ---")

    try:
        response = requests.get(URL, timeout=10) # Add a timeout for forecast request
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        API_data = response.json()

        # Check if 'list' key exists in the response (indicates successful forecast data)
        if 'list' not in API_data:
            print(f"Error: No forecast data found for {City}. Response: {API_data.get('message', 'Unknown error')}")
            API_data = None # Reset to None if data is not as expected
            print("Please re-enter the city name.")
            continue # Restart city loop to ask for input again

        # If we reach here, data was fetched successfully and contains 'list'
        print(f"Successfully fetched weather data for {City}.")
        break # Exit the city loop as valid data is obtained

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Error: City '{City}' not found. Please check the spelling.")
        elif response.status_code == 401:
            # This case should ideally not happen if API key was validated, but good to catch
            print("Error: API Key became invalid during city fetch. Please re-enter API Key and City.")
            # If API key suddenly becomes invalid, we might want to restart the whole process
            # For simplicity, we'll just ask for city again, but a more robust app might exit or re-validate key
            continue
        else:
            print(f"An HTTP error occurred during data fetch: {http_err} (Status Code: {response.status_code})")
            print("An API-specific error occurred. Please try a different city or check your internet.")
        print("Please re-enter the city name.")
        continue # Restart city loop

    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred during data fetch: {conn_err}. Please check your internet connection.")
        print("Please re-enter the city name.")
        continue # Restart city loop

    except requests.exceptions.Timeout as timeout_err:
        print(f"Request timed out during data fetch: {timeout_err}. The API might be slow or your connection is unstable.")
        print("Please re-enter the city name.")
        continue # Restart city loop

    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected request error occurred during data fetch: {req_err}")
        print("Please re-enter the city name.")
        continue # Restart city loop

    except json.JSONDecodeError:
        print("Error: Could not decode JSON response from API. Response might not be valid JSON.")
        print("Please re-enter the city name.")
        continue # Restart city loop

    except Exception as e:
        print(f"An unexpected error occurred during data fetch: {e}")
        print("Please re-enter the city name.")
        continue # Restart city loop

# Initialize list for cleaned data (moved here as it's dependent on successful API data)
cleaned_data_list = []

# --- Helper Function: Check if a string can be converted to a number ---
def is_numeric(value):
    """
    Checks if a given string value can be converted to an integer or float.
    Returns True if convertible, False otherwise.
    """
    try:
        # Try converting to integer first
        int(value)
        return True
    except ValueError:
        try:
            # If not an integer, try converting to float
            float(value)
            return True
        except ValueError:
            # If neither, it's not numeric
            return False

# Proceed only if API data was successfully fetched (guaranteed by the loop break)
# Extract time and temperature
time = [(item['dt_txt']) for item in API_data['list']]
# Convert Kelvin to Celsius and round to 2 decimal places
temp = [round(item['main']['temp'] - 273.15, 2) for item in API_data['list']]

# --- Step 2: Cleaning ---
# The 'temp' list from OpenWeatherMap should ideally contain only numbers.
# However, we'll keep the cleaning logic for robustness against unexpected data.
cleaning_list = temp # The list to be cleaned

print("\n--- Cleaning Data from List ---")
for item in cleaning_list:
    # Convert item to string to ensure is_numeric can process it
    # This is mainly for robustness if 'item' somehow isn't a string or number
    item_str = str(item).strip()

    if is_numeric(item_str):
        # If it's numeric, convert it to float (as temperatures often have decimals)
        # No need for nested try-except here, as is_numeric already confirmed it's convertible
        cleaned_value = float(item_str)
    else:
        # If not numeric, replace with the default value
        cleaned_value = DEFAULT_NUMERIC_VALUE
        print(f"  Replaced non-numeric '{item_str}' with {DEFAULT_NUMERIC_VALUE}.")
    cleaned_data_list.append(cleaned_value)

# --- Step 3: Convert to NumPy Array and Perform Analysis ---
if cleaned_data_list:
    # For a 1D list, direct conversion to NumPy array is straightforward
    cleaned_np_array = np.array(cleaned_data_list)
    print(f"\n--- Cleaned Data as NumPy Array (Shape: {cleaned_np_array.shape}) ---")
    print(cleaned_np_array)

    # Step 4: Perform Basic Statistical Analysis using NumPy
    print("\n--- Basic Statistical Analysis ---")
    print(f"Mean Temperature: {np.mean(cleaned_np_array):.2f}°C")
    print(f"Median Temperature: {np.median(cleaned_np_array):.2f}°C")
    print(f"Sum of Temperatures: {np.sum(cleaned_np_array):.2f}°C")
    print(f"Minimum Temperature: {np.min(cleaned_np_array):.2f}°C")
    print(f"Maximum Temperature: {np.max(cleaned_np_array):.2f}°C")
    print(f"Standard Deviation of Temperatures: {np.std(cleaned_np_array):.2f}°C")

else:
    print("No valid numerical data was cleaned or processed.")

# --- Step 5: Show Temperature Forecast in City ---
print(f"\nTemperature forecast in {City}:")
# Ensure 'time' and 'temp' lists are populated before zipping
if time and temp and len(time) == len(temp):
    for t, tp in zip(time, temp):
        print(f"{t}: {tp}°C")
else:
    print("Could not display detailed forecast due to missing or inconsistent data.")

