import pandas as pd
import os
from datetime import datetime
import glob

columns_to_extract = ['Patient Name', 'Patient ID', 'Sex','Index', 'Reason', 'Sys', 'Dia', 'HR', 'Mean', 'Hour', 'Minute', 'Month', 'Day', 'Year', 'Tag', 'Comments', 'Collection Stage']

def extract_patient_info_from_footer(asc_data, delim):
    patient_name = None
    patient_id = None
    sex_type = None

    # Looking for the line containing "Patient Name" and "Patient ID"
    for i, line in enumerate(asc_data):
        if "Patient Name" in line and "Patient ID" in line and "Sex" in line:
            # The next line contains the actual patient data
            patient_info_line = asc_data[i + 1].split(delim)  # Split by delimiter
            patient_name = patient_info_line[0].strip()
            patient_id = patient_info_line[1]  # Extracting Patient ID
            sex_type = patient_info_line[3]
            break
    return patient_name, patient_id, sex_type

# Function to read stages from the ASC file and assign them to indices
def read_stages_from_asc(asc_data, delim):
    stages = {}
    current_stage = None
    indices_in_stage = 0
    reading_indices = False
    i = 0


    while i < len(asc_data):
        cleaned_line = asc_data[i].strip()
        # Detect the stage headers
        if "Edited Awake BP Data Record Count" in cleaned_line:
            current_stage = "Edited Awake BP"
        elif "Edited Asleep BP Data Record Count" in cleaned_line:
            current_stage = "Edited Asleep BP"
        elif "Omitted Awake BP Data Record Count" in cleaned_line:
            current_stage = "Omitted Awake BP"
        elif "Omitted Asleep BP Data Record Count" in cleaned_line:
            current_stage = "Omitted Asleep BP"


        # Read the number of indices after the stage header
        if current_stage and cleaned_line.isdigit():
            indices_in_stage = int(cleaned_line)

            # If the number of indices is zero, skip this stage
            if indices_in_stage == 0:
                current_stage = None
            else:
                # Skip the next two lines (header and "Index, Reason, Sys, etc.")
                i += 2
                reading_indices = True  # Start reading indices

        # Read the actual indices for the stage
        if reading_indices:
            if cleaned_line.startswith("Index"):
                i += 1
                continue  # Skip the header line for indices
            cleaned_line = asc_data[i].strip()

            if cleaned_line and cleaned_line[0].isdigit():
                index = int(cleaned_line.split(delim)[0])
                stages[index] = current_stage
                indices_in_stage -= 1

                # Stop reading indices when the count reaches zero
                if indices_in_stage == 0:
                    reading_indices = False
                    current_stage = None
        i += 1
    return stages

# Function to count non-missing values in a row
def count_non_missing(row): # Count the number of fields that are not '--' or NaN
    return sum((x != '--' and pd.notna(x)) for x in row)

def process_asc_file_with_all_indices(asc_data):
    processed_data = []
    headers_found = False
    seen_indices = set()
    last_index = 0
    #current_stage = None  

    # Check for delimiter
    if ',' in asc_data[2]:
        delim = ','
    else:
        delim = '\t'

    patient_name, patient_id, sex_type = extract_patient_info_from_footer(asc_data, delim)
  
    stages = read_stages_from_asc(asc_data, delim)

    for line in asc_data:
        if headers_found:
            line_data = line.strip().split(delim)
            if len(line_data) >= 14 and line_data[0].isdigit():  # Ensure the index is numeric
                index = int(line_data[0])

                # Fill missing indices between the last index and the current one
                for missing_index in range(last_index + 1, index):
                    processed_data.append({
                        'Index': str(missing_index),
                        'Reason': '--',
                        'Sys': '--',
                        'Dia': '--',
                        'HR': '--',
                        'Mean': '--',
                        'Hour': '--',
                        'Minute': '--',
                        'Month': '--',
                        'Day': '--',
                        'Year': '--',
                        'Tag': '--',
                        'Comments': '--',
                        'Patient Name': patient_name,
                        'Patient ID': patient_id,
                        'Sex': sex_type,
                        'Collection Stage': stages.get(missing_index, '--')
                    })
                seen_indices.add(index)

                if len(line_data) >= 23:
                    processed_data.append({
                        'Patient Name': patient_name,
                        'Patient ID': patient_id,
                        'Sex': sex_type,
                        'Index': line_data[0],
                        'Reason': line_data[1],
                        'Sys': line_data[2],
                        'Dia': line_data[3],
                        'HR': line_data[4],
                        'Mean': line_data[5],
                        'Hour': line_data[14],
                        'Minute': line_data[15],
                        'Month': line_data[16],
                        'Day': line_data[17],
                        'Year': line_data[18],
                        'Tag': line_data[22],
                        'Comments': line_data[23] if len(line_data) > 23 else '',
                        'Collection Stage': stages.get(index, '--')
                    })
                else:
                    processed_data.append({
                        'Patient Name': patient_name,
                        'Patient ID': patient_id,
                        'Sex': sex_type,
                        'Index': line_data[0],
                        'Reason': line_data[1],
                        'Sys': line_data[2],
                        'Dia': line_data[3],
                        'HR': line_data[4],
                        'Mean': line_data[5],
                        'Hour': line_data[6],
                        'Minute': line_data[7],
                        'Month': line_data[8],
                        'Day': line_data[9],
                        'Year': line_data[10],
                        'Tag': line_data[12],
                        'Comments': line_data[13] if len(line_data) > 13 else '',
                        'Collection Stage': stages.get(index, '--')
                    })
                last_index = index
        elif line.startswith('Index'):
            headers_found = True

    df = pd.DataFrame(processed_data, columns=columns_to_extract)

    df['Index'] = pd.to_numeric(df['Index'], errors='coerce')

    df = df.dropna(subset=['Index'])
    # print(df)

    # Group by 'Index' and keep the row with the most filled data
    cleaned_df = df.loc[df.groupby('Index').apply(lambda x: x.apply(count_non_missing, axis=1).idxmax(), include_groups=False)]

    return cleaned_df

def list_patient_measurements(df, output_measurements_file):
    #  'Month', 'Day', and 'Year' are numeric
    df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
    df['Day'] = pd.to_numeric(df['Day'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    # Drop rows with NaN values in these columns (if any)
    df = df.dropna(subset=['Month', 'Day', 'Year'])

    # Group by Patient Name, Patient ID, and the date (Month, Day, Year)
    grouped = df.groupby(['Patient Name', 'Patient ID', 'Month', 'Day', 'Year']).size().reset_index(name='Measurements Count')

    patient_day_counts = grouped.groupby(['Patient Name', 'Patient ID']).size().reset_index(name = 'Days')

    # Open the output file for writing (CSV or TXT)
    with open(output_measurements_file, 'w') as f:
        current_patient = None
        days_count = 0

        # Iterate over the grouped data and write it to the file
        for _, row in grouped.iterrows():
            patient_name = row['Patient Name']
            patient_id = row['Patient ID']
            date = f"{int(row['Month'])}/{int(row['Day'])}/{int(row['Year'])}"
            measurements_count = row['Measurements Count']


            if (patient_name, patient_id) != current_patient:
                if current_patient is not None:
                    f.write("\n")

                days_count = patient_day_counts[(patient_day_counts['Patient Name'] == patient_name) & (patient_day_counts['Patient ID'] == patient_id)]['Days'].values[0]
                    
                print(f"\n{patient_name}, {patient_id}, Days: {days_count}")
                f.write(f"\n{patient_name}, {patient_id}, Days: {days_count}\n")
                current_patient = (patient_name, patient_id)

            # Also print the results
            print(f"date: {date} : {measurements_count} measurements")
            f.write(f"date: {date}, {measurements_count} measurements\n")
    print(f"Saved measurements summary to {output_measurements_file}")


def process_and_merge_asc_files_in_folder(folder_path):
    merged_data = pd.DataFrame(columns=columns_to_extract)

    asc_files = glob.glob(os.path.join(folder_path, '**', '*.asc'), recursive=True)

    if not asc_files:
        print("No .asc files found in the given directory or subdirectories.")
        return
   
    for file_path in asc_files:
        print(f"Processing file: {file_path}")
        with open(file_path, 'r') as file:
            asc_data = file.readlines()
        processed_data = process_asc_file_with_all_indices(asc_data)
        merged_data = pd.concat([merged_data, processed_data], ignore_index=True).drop_duplicates()

    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    if not os.path.isdir(os.path.join(folder_path, "output")):
            os.mkdir(os.path.join(folder_path, "output"))
    output_file = os.path.join(folder_path, "output", f'merged_processed_data_{timestamp}.csv')
    output_measurements_file = os.path.join(folder_path, "output", f'measurements_summary_{timestamp}.csv')  

    merged_data.to_csv(output_file, index=False)
    print(f"Saved merged processed data to {output_file}")

    # Call function to list patient measurements and save them to a TXT or CSV
    list_patient_measurements(merged_data, output_measurements_file)
# 

folder_path = input("Please indicate the folder that has the data to be processed or press enter to process all files in this folder (including subfolders): ")
while not os.path.isdir(folder_path) and folder_path:
    folder_path = input("Invalid folder path. Please indicate the folder that has the data to be processed or press enter to process all files in this folder (including subfolders): ")
if not folder_path:
    folder_path = os.getcwd()

process_and_merge_asc_files_in_folder(folder_path)



'''
asc_file_path = 'DuoResults2.asc'
with open(asc_file_path, 'r') as file:
    asc_data = file.readlines()

processed_data = process_asc_file_with_all_indices(asc_data)
# Select rows 0 to 30 and columns 0 to 15 
selected_data = processed_data.iloc[0:30, :]

selected_data.to_csv('processed_duo_results_with_patient_info5.csv', index=False)
print(selected_data)
'''




