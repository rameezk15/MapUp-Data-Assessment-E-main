import os
import requests
from dotenv import load_dotenv
import json
import argparse

load_dotenv()

api_key = os.getenv('TOLLGURU_API_KEY')
api_url = os.getenv('TOLLGURU_API_URL')
headers = {'x-api-key': api_key, 'Content-Type': 'csv'}

def process_csv_files(input_path, output_path):
    output_path = output_path.rstrip('/')  # Remove trailing slash if present

    for file_name in os.listdir(input_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(input_path, file_name)

            with open(file_path, 'rb') as csv_file:
                try:
                    response = requests.post(api_url, data=csv_file, headers=headers)
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    json_data = response.json()

                    response_filename = os.path.splitext(file_name)[0] + ".json"
                    response_path = os.path.join(output_path, response_filename)

                    with open(response_path, 'w') as json_file:
                        json.dump(json_data, json_file, indent=2)
                    
                    print(f"Successfully processed {file_name}")
                except requests.RequestException as e:
                    print(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process CSV files and save results as JSON.")
    parser.add_argument("--to_process", required=True, help="Path to the CSV folder.")
    parser.add_argument("--output_dir", required=True, help="The folder where the resulting JSON files will be stored.")
    args = parser.parse_args()

    # Process CSV files
    process_csv_files(args.to_process, args.output_dir)
