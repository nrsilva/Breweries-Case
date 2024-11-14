import requests
import json
import os
import pandas as pd
from datetime import datetime

# URL for the Open Brewery DB API
API_URL = "https://api.openbrewerydb.org/breweries"

# Path where raw data will be stored (bronze layer)
DATA_DIR = os.path.join(os.getcwd(), 'data', 'raw')

# Function to ensure the data directory exists
def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

# Function to fetch data from the API
def fetch_data_from_api(url: str, params: dict = None):
    """
    Function to consume data from the Open Brewery DB API.

    Args:
        url (str): API URL.
        params (dict, optional): Additional parameters for the GET request.

    Returns:
        list: List of JSON data returned by the API.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Will raise an error for non-200 status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching data from API: {e}")
        raise

# Function to save the raw data to a file
def save_data_to_file(data: list, filename: str):
    """
    Function to save raw data to a JSON or CSV file in the bronze layer.

    Args:
        data (list): Data to be saved to the file.
        filename (str): Name of the file to be saved.
    """
    file_path_json = os.path.join(DATA_DIR, filename + ".json")
    file_path_csv = os.path.join(DATA_DIR, filename + ".csv")

    try:
        # Save data as JSON
        with open(file_path_json, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        # Save data as CSV using Pandas
        df = pd.DataFrame(data)
        df.to_csv(file_path_csv, index=False)

        print(f"Data saved in {file_path_json} and {file_path_csv}")
    except Exception as e:
        print(f"Error while saving data to file: {e}")
        raise

# Main function to ingest data
def ingest_data():
    # Ensure the data directory exists
    ensure_data_dir()

    # Define parameters for the API request (can be adjusted for pagination or filtering)
    params = {"per_page": 50}  # Example: Show 50 breweries per page

    # Fetch data from the API
    print("Fetching data from Open Brewery DB API...")
    breweries_data = fetch_data_from_api(API_URL, params=params)

    # Generate a filename with the current timestamp to avoid overwriting files
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"breweries_{timestamp}"

    # Save the fetched data to a file
    save_data_to_file(breweries_data, filename)

# Execute the ingestion pipeline
if __name__ == "__main__":
    ingest_data()
