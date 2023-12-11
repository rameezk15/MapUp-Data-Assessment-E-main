import argparse
import pandas as pd
import os

def read_parquet_file(file_path):
    """
    Reads a parquet file and returns a pandas DataFrame.

    Parameters:
    - file_path (str): Path to the parquet file.

    Returns:
    - pd.DataFrame: DataFrame containing the data from the parquet file.
    """
    return pd.read_parquet(file_path)

def process_trip_data(trip_data, output_dir):
    """
    Process trip data, calculate time differences, assign trip numbers, and save subsets.

    Parameters:
    - trip_data (pd.DataFrame): DataFrame containing trip data.
    - output_dir (str): Folder to store the resulting CSV files.

    Returns:
    None
    """
    # Convert timestamp to datetime
    trip_data['timestamp'] = pd.to_datetime(trip_data['timestamp'])

    # Calculate time differences in hours
    trip_data['time_diff'] = trip_data['timestamp'].diff().dt.total_seconds() // 3600

    # Identify time boundaries for trips
    time_boundaries = trip_data['time_diff'] > 7

    # Assign trip numbers based on time boundaries
    trip_data['trip_number'] = time_boundaries.cumsum()

    # Process each trip and save subsets
    for trip_number, trip_data_subset in trip_data.groupby('trip_number'):
        unit = trip_data_subset['unit'].iloc[0]

        # Format timestamp to string
        trip_data_subset['timestamp'] = trip_data_subset['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        # Select relevant columns for the subset
        subset_columns = ['latitude', 'longitude', 'timestamp']
        trip_data_subset = trip_data_subset[subset_columns]

        # Save subset to CSV file
        subset_filename = os.path.join(output_dir, f"{unit}_{trip_number}.csv")
        trip_data_subset.to_csv(subset_filename, index=False)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process Parquet file and save trip subsets to CSV.")
    parser.add_argument("--to_process", required=True, help="Path to the Parquet file to be processed.")
    parser.add_argument("--output_dir", required=True, help="The folder to store the resulting CSV files.")
    args = parser.parse_args()

    # Read parquet file
    trip_data = read_parquet_file(args.to_process)

    # Process trip data
    process_trip_data(trip_data, args.output_dir)