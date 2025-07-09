import os

#File_name for dummy file
DATA_FILENAME = "raw_data.txt"

# Define the default value to replace non-numeric entries.
DEFAULT_NUMERIC_VALUE = 0

# Helper Function: Check if a string can be converted to a number
def is_numeric(value):
    """
    Checks if a given string value can be converted to an integer or float.
    Returns True if convertible, False otherwise.
    """
    try:
        # Try converting to integer first, then float
        int(value)
        return True
    except ValueError:
        try:
            float(value)
            return True
        except ValueError:
            return False

# Step 1: Prepare the "raw_data.txt" file
# We'll create a dummy file with some mixed data for demonstration.
# In a real scenario, this file would be provided or collected from a source.

sample_data_content = "[1,2,3,4,5,6,7,9,str,10.5,invalid_text,12,None,8]\n" \
                      "[11,22,another_str,33,44,55]\n" \
                      "[60,70,80,final_text]"

print(f"--- Preparing '{DATA_FILENAME}' with sample data ---")

with open(DATA_FILENAME, 'w') as f:
    f.write(sample_data_content)

print(f"Sample data written to '{DATA_FILENAME}'.\n")

# Step 2: Read Data from the File
# This section reads each line from the specified data file.

print(f"--- Reading data from '{DATA_FILENAME}' ---")
raw_lines = []

try:
    with open(DATA_FILENAME, 'r') as f:
        raw_lines = f.readlines()
    print("Data read successfully.")

except FileNotFoundError:
    print(f"Error: The file '{DATA_FILENAME}' was not found.")
    raw_lines = [] # Ensure raw_lines is empty on error

except Exception as e:
    print(f"An unexpected error occurred while reading the file: {e}")
    raw_lines = []

# Step 3: Process and Clean the Data
# This is the core cleaning logic.
cleaned_data_list = []

if raw_lines:
    print("\n--- Cleaning and Transforming Data ---")
    for line_num, line in enumerate(raw_lines):
        # Remove leading/trailing whitespace and brackets, then split by comma
        # Example: "[1,2,str]" -> "1,2,str" -> ["1", "2", "str"]
        # .strip('[]\n') removes square brackets and newline characters
        processed_line = line.strip().strip('[]').split(',')

        current_cleaned_row = []
        for item_str in processed_line:
            # Clean each string item: remove leading/trailing spaces
            item_str = item_str.strip()

            # Check if the item can be converted to a number
            if is_numeric(item_str):
                try:
                    # Attempt to convert to int, if fails, convert to float
                    cleaned_value = int(item_str)
                except ValueError:
                    cleaned_value = float(item_str)
            else:
                # If not numeric, replace with the default value
                cleaned_value = DEFAULT_NUMERIC_VALUE
                print(f"  Line {line_num+1}: Replaced '{item_str}' with {DEFAULT_NUMERIC_VALUE}")

            current_cleaned_row.append(cleaned_value)
        cleaned_data_list.append(current_cleaned_row)
else:
    print("No raw data lines to process.")

# Step 4: Display Results
print("\n--- Original Data (as read from file lines) ---")
for line in raw_lines:
    print(line.strip()) # strip to remove extra newlines for cleaner output

print("\n--- Cleaned and Transformed Data ---")
for row in cleaned_data_list:
    print(row)


# Step 5: Clean up: Remove the dummy file
if os.path.exists(DATA_FILENAME):
     os.remove(DATA_FILENAME)
     print(f"\nCleaned up: Removed '{DATA_FILENAME}'.")
