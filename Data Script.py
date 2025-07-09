import os
import numpy as np # Import NumPy

# Configuration ---
DATA_FILENAME = "raw_data.txt"
DEFAULT_NUMERIC_VALUE = 0

# Helper Function: Check if a string can be converted to a number ---
def is_numeric(value):
    """
    Checks if a given string value can be converted to an integer or float.
    Returns True if convertible, False otherwise.
    """
    try:
        int(value)
        return True
    except ValueError:
        try:
            float(value)
            return True
        except ValueError:
            return False

# Step 1: Prepare the "raw_data.txt" file ---
sample_data_content = "[1,2,3,4,5,6,7,9,str,10.5,invalid_text,12,None,8]\n" \
                      "[11,22,another_str,33,44,55]\n" \
                      "[60,70,80,final_text]"

print(f"--- Preparing '{DATA_FILENAME}' with sample data ---")

with open(DATA_FILENAME, 'w') as f:
    f.write(sample_data_content)

print(f"Sample data written to '{DATA_FILENAME}'.\n")

# Step 2: Read Data from the File ---
print(f"--- Reading data from '{DATA_FILENAME}' ---")
raw_lines = []

try:
    with open(DATA_FILENAME, 'r') as f:
        raw_lines = f.readlines()
    print("Data read successfully.")

except FileNotFoundError:
    print(f"Error: The file '{DATA_FILENAME}' was not found.")
    raw_lines = []

except Exception as e:
    print(f"An unexpected error occurred while reading the file: {e}")
    raw_lines = []

# Step 3: Process and Clean the Data ---
cleaned_data_list = [] # This remains a Python list of lists during cleaning

if raw_lines:
    print("\n--- Cleaning and Transforming Data ---")
    for line_num, line in enumerate(raw_lines):
        processed_line = line.strip().strip('[]').split(',')
        
        current_cleaned_row = []
        for item_str in processed_line:
            item_str = item_str.strip()
            
            if is_numeric(item_str):
                try:
                    cleaned_value = int(item_str)
                except ValueError:
                    cleaned_value = float(item_str)
            else:
                cleaned_value = DEFAULT_NUMERIC_VALUE
                print(f"  Line {line_num+1}: Replaced '{item_str}' with {DEFAULT_NUMERIC_VALUE}")
            
            current_cleaned_row.append(cleaned_value)
        cleaned_data_list.append(current_cleaned_row)
else:
    print("No raw data lines to process.")

# NEW STEP: Convert cleaned_data_list to a NumPy array
# This happens AFTER all cleaning is done and cleaned_data_list is fully populated.
if cleaned_data_list:
    # Ensure all rows have the same number of columns for a rectangular NumPy array
    max_cols = max(len(row) for row in cleaned_data_list)
    # Pad shorter rows with default value to make them rectangular
    padded_data_list = [row + [DEFAULT_NUMERIC_VALUE] * (max_cols - len(row)) for row in cleaned_data_list]
    
    cleaned_np_array = np.array(padded_data_list)
    print(f"\n--- Cleaned Data as NumPy Array (Shape: {cleaned_np_array.shape}) ---")
    print(cleaned_np_array)

    # Step 4: Perform Basic Statistical Analysis using NumPy
    print("\n--- Basic Statistical Analysis ---")
    print(f"Mean of all data: {np.mean(cleaned_np_array):.2f}")
    print(f"Median of all data: {np.median(cleaned_np_array):.2f}")
    print(f"Sum of all data: {np.sum(cleaned_np_array):.2f}")
    print(f"Minimum value: {np.min(cleaned_np_array):.2f}")
    print(f"Maximum value: {np.max(cleaned_np_array):.2f}")
    print(f"Standard Deviation: {np.std(cleaned_np_array):.2f}")

else:
    print("No data to convert to NumPy array or perform analysis.")

Clean up: Remove the dummy file (optional)
if os.path.exists(DATA_FILENAME):
os.remove(DATA_FILENAME)
print(f"\nCleaned up: Removed '{DATA_FILENAME}'.")

