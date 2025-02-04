import pandas as pd
import os
import glob
# Define the columns to extract including the new one: Collection Stage
columns_to_extract = ['Patient Name', 'Patient ID', 'Sex', 'Index', 'Reason', 'Sys', 'Dia', 'HR', 'Mean',
                      'Hour', 'Minute', 'Month', 'Day', 'Year', 'Tag', 'Comments', 'Collection Stage']
# Function to extract patient information (name, ID, sex) from the footer of the ASC file
def extract_patient_info_from_footer(asc_data, delim):
    patient_name = None
    patient_id = None
    sex_type = None
    # Looking for the line containing "Patient Name" and "Patient ID"
    for i, line in enumerate(asc_data):
        if "Patient Name" in line and "Patient ID" in line and "Sex" in line:
            # The next line contains the actual patient data
            patient_info_line = asc_data[i + 1].split(delim)  # Split by whitespace or tabs
            patient_name = patient_info_line[0].strip() # Extracting Patient Name (First + Last)
            patient_id = patient_info_line[1]  # Extracting Patient ID
            sex_type = patient_info_line[3]  # Extracting Sex
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
def count_non_missing(row):
    return sum((x != '--' and pd.notna(x)) for x in row)
# Main processing function for ASC file
def process_asc_file_with_stages_and_all_indices(asc_data):
    processed_data = []
    headers_found = False
    seen_indices = set()
    last_index = 0

    # Check for delimiter
    if ',' in asc_data[2]:
        delim = ','
    else:
        delim = '\t'

    # Extract patient information from the footer of the ASC file
    patient_name, patient_id, sex_type = extract_patient_info_from_footer(asc_data, delim)
    # Extract stages for the indices from the ASC file
    stages = read_stages_from_asc(asc_data, delim)
    # Process each line to gather data
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
    # Convert the processed data into a DataFrame
    df = pd.DataFrame(processed_data, columns=columns_to_extract)
    # Ensure the 'Index' column is numeric and drop rows with NaN indices
    df['Index'] = pd.to_numeric(df['Index'], errors='coerce')
    df = df.dropna(subset=['Index'])
    # Group by 'Index' and keep the row with the most filled data
    cleaned_df = df.loc[df.groupby('Index').apply(lambda x: x.apply(count_non_missing, axis=1).idxmax())]
    return cleaned_df

# Function to process all ASC files in a directory
def process_all_asc_files_in_folder(folder_path):

    asc_files = glob.glob(os.path.join(folder_path, '**', '*.asc'), recursive=True)

    if not asc_files:
        print("No .asc files found in the given directory or subdirectories.")
        return

    # Loop through all .asc files in the folder
    for file_path in asc_files:
        print(f"Processing file: {file_path}")
        # Load the ASC file
        with open(file_path, 'r') as file:
            asc_data = file.readlines()
        # Process the ASC file with stages and all indices
        processed_data = process_asc_file_with_stages_and_all_indices(asc_data)
        # Save the processed data to a CSV file
        output_csv_file = file_path.replace('.asc', '_processed_with_stages.csv')
        processed_data.to_csv(output_csv_file, index=False)
        print(f"Saved processed data with stages to {output_csv_file}")

# Example usage
folder_path = input("Please indicate the folder that has the data to be processed or press enter to process all files in this folder (including subfolders): ")
while not os.path.isdir(folder_path) and folder_path:
    folder_path = input("Invalid folder path. Please indicate the folder that has the data to be processed or press enter to process all files in this folder (including subfolders): ")
if not folder_path:
    folder_path = os.getcwd()

process_all_asc_files_in_folder(folder_path)