import pandas as pd
import glob
import os
from datetime import datetime


def list_patient_measurements(merged_data_file):
    # Load the merged data CSV file
    df = pd.read_csv(merged_data_file)
    print(df)
    # Ensure that 'Month', 'Day', and 'Year' are numeric
    df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
    df['Day'] = pd.to_numeric(df['Day'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    # Drop rows with NaN values in these columns (if any)
    df = df.dropna(subset=['Month', 'Day', 'Year'])
    # Group by Patient Name, Patient ID, and the date (Month, Day, Year)
    grouped = df.groupby(['Patient Name', 'Patient ID', 'Month', 'Day', 'Year']).size().reset_index(name='Measurements Count')
    # Create an output dictionary to store the results
    output_dict = {}
    for _, row in grouped.iterrows():
        patient_name = row['Patient Name']
        patient_id = row['Patient ID']
        date = f"{int(row['Month'])}/{int(row['Day'])}/{int(row['Year'])}"
        measurements_count = row['Measurements Count']
        # Initialize patient entry if not exists
        if (patient_name, patient_id) not in output_dict:
            output_dict[(patient_name, patient_id)] = []
        # Append the measurement date and count to the patient's entry
        output_dict[(patient_name, patient_id)].append(f"date: {date} : {measurements_count} measurements")
    # Print the results
    for (patient_name, patient_id), measurements in output_dict.items():
        print(f"\n{patient_name}, {patient_id}")
        for measurement in measurements:
            print(measurement)

# Example usage
# merged_data_file = 'merged_processed_data.csv'  # Replace with your merged data file path
max_datetime = datetime.min
files_dict = {}

merged_data_files = glob.glob("**/merged_processed_data*.csv", recursive=True)

if not merged_data_files:
    merged_data_file = input("No merged data files found in current directory. Enter merged data file path: ")
    while not os.path.isfile(merged_data_file):
        merged_data_file = input("Invalid file path. Enter merged data file path: ")
    if not 'merged_processed_data' in merged_data_file:
        choice = input('Warning: the given file path does not include "merged_processed_data". Would you like to proceed? (y/n) ')
        while choice != 'y' and choice != 'n' and choice != 'Y' and choice != 'N':
            choice = input('Invalid input. Warning: the given file path does not include "merged_processed_data". Would you like to proceed? (y/n)')
        if choice == 'n' or choice == 'N':
            merged_data_file = input("Enter merged data file path: ")
            while not os.path.isfile(merged_data_file):
                merged_data_file = input("Invalid file path. Enter merged data file path: ")
else:
    for filepath in merged_data_files:
        filename = os.path.basename(filepath)
        filename_parts = filename.split('_')
        datetime_str = filename_parts[3] + filename_parts[4]

        year = int(datetime_str[:4])
        month = int(datetime_str[4:6])
        day = int(datetime_str[6:8])
        hour = int(datetime_str[8:10])
        minute = int(datetime_str[10:12])

        datetime_obj = datetime(year, month, day, hour=hour, minute=minute)
        files_dict[datetime_obj] = filepath

        if datetime_obj > max_datetime:
            max_datetime = datetime_obj

    merged_data_file = input("Merged data files found. Hit Enter/Return to use most recent data from " + str(max_datetime) + " or enter merged data file path: ")
    while not os.path.isfile(merged_data_file) and merged_data_file:
        merged_data_file = input("Invalid file path. Hit Enter/Return to use most recent data from " + str(max_datetime) + " or enter merged data file path: ")
    if not merged_data_file:
        merged_data_file = files_dict[max_datetime]
    if not 'merged_processed_data' in merged_data_file:
        choice = input('Warning: the given file path does not include "merged_processed_data". Would you like to proceed? (y/n) ')
        while choice != 'y' and choice != 'n' and choice != 'Y' and choice != 'N':
            choice = input('Invalid input. Warning: the given file path does not include "merged_processed_data". Would you like to proceed? (y/n)')
        if choice == 'n' or choice == 'N':
            merged_data_file = input("Enter merged data file path: ")
            while not os.path.isfile(merged_data_file):
                merged_data_file = input("Invalid file path. Enter merged data file path: ")


print(merged_data_file)



# merged_data_file = input("Enter the merged data file path: ")


list_patient_measurements(merged_data_file)