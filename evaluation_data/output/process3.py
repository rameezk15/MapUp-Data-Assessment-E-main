import os
import argparse
import pandas as pd
import json

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None

def process_trip_data(trip, trip_id, unit):
    start_info = trip.get('start', {})
    end_info = trip.get('end', {})

    return {
        'unit': unit,
        'trip_id': trip_id,
        'toll_loc_id_start': start_info.get('id', ''),
        'toll_loc_id_end': end_info.get('id', ''),
        'toll_loc_name_start': start_info.get('name', ''),
        'toll_loc_name_end': end_info.get('name', ''),
        'toll_system_type': trip.get('type', ''),
        'entry_time': start_info.get('timestamp_formatted', ''),
        'exit_time': end_info.get('timestamp_formatted', ''),
        'tag_cost': trip.get('tagCost', ''),
        'cash_cost': trip.get('cashCost', ''),
        'license_plate_cost': trip.get('licensePlateCost', '')
    }

def process_files(input_folder):
    trip_data_list = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            trip_id = filename.split('.')[0]
            unit = trip_id.split('_')[0]
            file_location = os.path.join(input_folder, filename)
            json_data = load_json_file(file_location)

            toll_data = json_data.get('route', {}).get('tolls', [])
            if len(toll_data) != 0:
                for trip in toll_data:                    
                    trip_data_list.append(process_trip_data(trip, trip_id, unit))
    return trip_data_list

def save_to_csv(data, output_folder):
    df = pd.DataFrame(data)
    csv_file_path = os.path.join(output_folder, "transformed_data.csv")
    
    try:
        df.to_csv(csv_file_path, index=False)
        print(f"CSV file saved successfully at {csv_file_path}")
    except IOError as e:
        print(f"Error saving CSV file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Process JSON files and save results as CSV.")
    parser.add_argument("--to_process", required=True, help="Path to the JSON responses folder.")
    parser.add_argument("--output_dir", required=True, help="The folder where the resulting CSV file will be stored.")
    args = parser.parse_args()

    input_folder, output_folder = args.to_process, args.output_dir

    if not os.path.exists(input_folder) or not os.path.isdir(input_folder):
        print(f"Input folder {input_folder} does not exist or is not a directory.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    trip_data_list = process_files(input_folder)
    save_to_csv(trip_data_list, output_folder)

if __name__ == "__main__":
    main()