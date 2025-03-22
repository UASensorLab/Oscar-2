import pandas as pd
import os
def read_stages_from_asc(asc_file):
    stages = {}
    current_stage = None
    indices_in_stage = 0
    reading_indices = False
    index_count_verified = False
    with open(asc_file, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            cleaned_line = lines[i].strip()
            # Detect the stage headers
            if "Edited Awake BP Data Record Count" in cleaned_line:
                current_stage = "Edited Awake BP"
                print(f"Stage detected: {current_stage}")
            elif "Edited Asleep BP Data Record Count" in cleaned_line:
                current_stage = "Edited Asleep BP"
                print(f"Stage detected: {current_stage}")
            elif "Omitted Awake BP Data Record Count" in cleaned_line:
                current_stage = "Omitted Awake BP"
                print(f"Stage detected: {current_stage}")
            elif "Omitted Asleep BP Data Record Count" in cleaned_line:
                current_stage = "Omitted Asleep BP"
                print(f"Stage detected: {current_stage}")


            # Read the number of indices after the stage header
            if current_stage and cleaned_line.isdigit():
                indices_in_stage = int(cleaned_line)
                print(f"Expecting {indices_in_stage} indices for stage {current_stage}")
                # If the number of indices is zero, skip this stage
                if indices_in_stage == 0:
                    current_stage = None  # Reset the stage
                    print(f"Skipped stage {current_stage} with 0 indices")
                else:
                    # Skip the next two lines (header and "Index, Reason, Sys, etc.")
                    i += 2
                    reading_indices = True  # Start reading indices
            # Read the actual indices for the stage
            if reading_indices:
                if cleaned_line.startswith("Index"):
                    # Skip the header line for indices
                    i += 1
                    continue
                # Begin reading the actual indices
                cleaned_line = lines[i].strip()
                if cleaned_line and cleaned_line[0].isdigit():
                    index = int(cleaned_line.split('\t')[0])
                    stages[index] = current_stage
                    print(f"Assigned index {index} to stage {current_stage}")
                    indices_in_stage -= 1
                    # Stop reading indices when the count reaches zero
                    if indices_in_stage == 0:
                        reading_indices = False
                        current_stage = None  # Reset the stage after completing
                        print(f"Finished reading all indices for stage {current_stage}")
            i += 1  # Move to the next line
    return stages

# Function to match stages with the filtered data
def match_stages_with_filtered_data(filtered_df, stages):
    filtered_df['Collection Stage'] = filtered_df['Index'].map(stages).fillna('--')
    return filtered_df
# Function to process the ASC file and filter data
def process_and_filter_data(asc_file, filtered_data_file):
    # Step 1: Read stages from the ASC file
    stages = read_stages_from_asc(asc_file)
    # Step 2: Load the filtered data
    filtered_df = pd.read_csv(filtered_data_file)
    # Step 3: Match stages with the filtered data
    result_df = match_stages_with_filtered_data(filtered_df, stages)
    # Step 4: Save the updated data with Collection Stage column
    output_csv_file = filtered_data_file.replace('.csv', '_with_stages.csv')
    result_df.to_csv(output_csv_file, index=False)
    print(f"Saved processed data with stages to {output_csv_file}")
# Example usage
asc_file = 'Me Hi -9132024.asc'  # Replace with the actual ASC file path
filtered_data_file = 'Me Hi -9132024_processed.csv'  # Replace with your filtered data CSV
process_and_filter_data(asc_file, filtered_data_file)