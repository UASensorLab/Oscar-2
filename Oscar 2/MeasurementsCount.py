import pandas as pd
def list_patient_measurements(merged_data_file):
    # Load the merged data CSV file
    df = pd.read_csv(merged_data_file)
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
merged_data_file = 'merged_processed_data.csv'  # Replace with your merged data file path
list_patient_measurements(merged_data_file)