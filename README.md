# MapUp - Python Assessment

## Overview

This assessment evaluates your Python skills in following aspects - pandas data wrangling, API response retrieval, async programming, and JSON response manipulation. Your performance will be assessed on correctness against predefined test cases, execution runtime efficiency, and adherence to Python best practices.

The task involves constructing a robust data pipeline with three distinct processes, each executed by a dedicated Python script. The output of each process serves as the input for the subsequent one, creating a well-connected sequence of data processing steps.

This assessment provides an opportunity to showcase your Python skills and your capability to design effective and efficient data workflows. Best of luck!

## Process 1: Extracting trips from GPS Data

In this task, you are required to develop a Python script named `process1.py` that processes GPS data of multiple vehicles stored in a Parquet file. The objective is to extract information related to individual trips and store the results in CSV files. The Parquet file contains the following columns:

- **unit**: Unique identification of the vehicle.
- **latitude**: GPS latitude in degrees.
- **longitude**: GPS longitude in degrees.
- **timestamp**: Timestamp string in RFC 3301 format.

For each unique unit in the Parquet file, you need to break down the data into trip-specific CSV files. The script should use the following logic to identify trips:

- Whenever the time difference between consecutive data points is more than 7 hours, a new trip begins.

The naming convention for trip CSV files is as follows:

- CSV files should be named using the pattern `{unit}_{trip_number}.csv`.
- The trip numbering starts from 0 and increments for each new trip.

Each CSV file should contain the following columns:
- **latitude**: GPS latitude in degrees.
- **longitude**: GPS longitude in degrees.
- **timestamp**: Timestamp string in RFC 3301 format.

### Script Usage:

The Python script (`process1.py`) should be executed with the following command-line arguments:

- `--to_process`: Path to the Parquet file to be processed.
- `--output_dir`: The folder to store the resulting CSV files.

### Example Execution:

```bash
python3 process1.py --to_process /test/test.parquet --output_dir /output/process1
```

## Process 2: Uploading GPS tracks to TollGuru API

In the second process, your task is to develop a Python script to interact with the TollGuru API. The `gps-tracks-csv-upload` endpoint of the TollGuru API takes a vehicle as a parameter and expects a binary CSV file as input. The API responds with a JSON containing toll information.

### API Key and URL Configuration

To begin, sign up on [TollGuru](https://tollguru.com/get-api-key) to obtain your API KEY. Both the TOLLGURU_API_KEY and the TOLLGURU_API_URL should be stored in a `.env` file, and the `python-dotenv` module should be used to load these variables.

### API Parameters

When sending requests to the `gps-tracks-csv-upload` endpoint, use the following parameters:
- vehicleType: 5AxlesTruck
- mapProvider: osrm

### Sample Python Request

Here is an example python request illustrating how to send a request with the specified parameters:

```bash

import requests

url = 'https://apis.tollguru.com/toll/v2/gps-tracks-csv-upload?mapProvider=osrm&vehicleType=5AxlesTruck'
file_path = '/path/to/file.csv'
headers = {'x-api-key': 'YOUR_TRIAL_API_KEY', 'Content-Type': 'text/csv'}

with open(file_path, 'rb') as file:
    response = requests.post(url, data=file, headers=headers)
```
Your Python script should concurrently send CSV files obtained from Process1 to the TollGuru API, using the same file names for storage of the JSON responses.

### Script Usage:

The Python script (`process2.py`) should be executed with the following command-line arguments:

- `--to_process`: Path to the CSV folder.
- `--output_dir`: The folder where the resulting JSON files will be stored.

### Example Execution:

```bash
python3 process2.py --to_process /output/process1 --output_dir /output/process2
```

## Process 3: Extracting Toll Information from JSON Files

For the third process, you are assigned to develop a Python script that processes toll information stored in multiple JSON files. Each JSON file represents toll information for a specific trip, and the script needs to handle all files within the specified input directory.

### Data Extraction and CSV Transformation

The script should perform the following tasks for each trip's toll information:
- Extract relevant data from the JSON files.
- Transform the data into a CSV format with the following headers:

  - `unit`: Unique identification number for the vehicle.
  - `trip_id`: File name of each trip.
  - `toll_loc_id_start`: Toll ID for the start toll.
  - `toll_loc_id_end`: Toll ID for the end toll.
  - `toll_loc_name_start`: Name for the start toll.
  - `toll_loc_name_end`: Name for the end toll.
  - `toll_system_type`: Type of toll.
  - `entry_time`: Time of toll entry.
  - `exit_time`: Time of toll exit.
  - `tag_cost`: Tag cost of the toll.
  - `cash_cost`: Cash cost of the toll.
  - `license_plate_cost`: License plate cost of the toll.

### CSV Output

The script should consolidate the processed data and save the results in a single CSV file with file name `transformed_data.csv`

### Note

Handle cases where values might be null in the JSON files by leaving the corresponding fields empty in the CSV.

If there are no tolls in a route, you can ignore those files

Ensure that the script can efficiently process a large number of JSON files in the specified input directory.

### Script Usage:

The Python script (`process3.py`) should be executed with the following command-line arguments:

- `--to_process`: Path to the JSON responses folder.
- `--output_dir`: The folder where the final `transformed_data.csv` will be stored.


### Example Execution:

```bash
python3 process3.py --to_process /output/process2 --output_dir /output/process3
```


## Important Points to Note:

- All scripts must be developed in accordance with the specified rules.
- The assessment pipeline will be tested using our internal set of test cases.
- Throughput times and result validation will be key factors in the evaluation process.
- Incorporate unit tests into your scripts for extra credits.
- Any deviation especially in naming conventions and providing arguments will impact the correct assessment of your work


## Result Submission:
- We have provided a sample parquet file containing two trips and the pipeline results in sample_data folder.
- Data that you need to work with is `evaluation_data/input/raw_data.parquet`. Store your process outputs in the structure mentioned below
- Clone the provided GitHub repository.
- Add the following members as collaborators to your repo
    - `venkateshn@mapup.ai`
    - `namanjeetsingh@mapup.ai`
    - `saranshj@mapup.ai`
    - `varuna@mapup.ai`
- Submit the link to your repository via the provided Google Form for evaluation.


## Submission structure
- 📂 assessment
  - 📄 process1.py
  - 📄 process2.py
  - 📄 process3.py
  - 📂 evaluation_data
    - 📂 input
        - 📄 raw_data.parquet
    - 📂 output  
      - 📂 process1
        - 📄 output_file1.csv
        - 📄 output_file2.csv
        - ...
      - 📂 process2
        - 📄 output_file1.json
        - 📄 output_file2.json
        - ...
      - 📂 process3
        - 📄 transformed_data.csv

## MapUp - Excel Assessment

You have to submit an excel assessment along with your previous task. This evaluation tests your proficiency in Conditional Formatting, Excel Formulae, and Data Manipulation

### Instructions

1. Download the Excel assessment file (excel-assessment.xlsm) from your cloned repository.
2. Complete the assessment tasks as per the instructions provided within the spreadsheet.

## Submission

1. Upload the solved Excel file to your repository.
2. Submit the link to your repository via the provided Google Form for evaluation

We appreciate your attention to detail and commitment to following the guidelines. Good luck with your assessment!
