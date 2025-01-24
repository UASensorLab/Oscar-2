# Rewriting the README content to the file and ensuring it's accessible for download.

readme_content = """
# ASC File Processor and Measurement Summary Script

## Overview

This Python script processes `.asc` files containing patient blood pressure measurements, merges the data into a single CSV file, and summarizes the measurement dates for each patient. The output includes:

1. **Merged Data**: A CSV file containing all processed `.asc` files, including patient details and measurement data.
2. **Measurement Summary**: A separate file (`.txt` or `.csv`) listing each patient's measurement dates and the number of measurements per day, including the total number of unique days they were measured.

## Files Produced
- `merged_processed_data_{timestamp}.csv`: Contains all patient measurement data merged from multiple `.asc` files.
- `measurements_summary_{timestamp}.txt`: Lists the measurement dates and the number of measurements for each patient, with the number of unique days measured.

## Prerequisites

To use the script, you need to have Python installed on your system. You will also need the following Python packages:
- `pandas`

You can install `pandas` using pip:

```bash
pip install pandas
```

## How It Works

1. **Processing `.asc` Files**:
   - The script reads `.asc` files from a specified folder.
   - It extracts patient information (name, ID, sex), measurement data (such as systolic, diastolic pressure), and assigns a collection stage (e.g., `Edited Awake BP`).
   - The files are merged into a single CSV file.

2. **Summarizing Measurements**:
   - After merging the data, the script groups the measurements by patient and date, calculating the number of measurements per day.
   - The summary also includes the number of unique days each patient was measured.

## Folder Structure

- **ASC Files**: Store all your `.asc` files in one folder.
- **Output**: The script outputs two files:
  1. A CSV with the merged measurement data.
  2. A file with the measurement summary (can be `.txt` or `.csv`).

## Usage

### 1. Run the Script

Simply run the Python script to process the `.asc` files and generate the outputs.

```bash
python process_asc_files.py
```

### 2. Enter the Path to .asc Directory

When you run the script, the system will prompt you to enter the path to the directory containing the .asc files. To use the directory from which you are running the script (current working directory), simply hit enter. The script will automatically search the provided directory, as well as any subdirectories, for .asc files.

### 3. Outputs

After running the script, you will see two outputs:

1. **Merged Data CSV**: A CSV file (`merged_processed_data_{timestamp}.csv`) with the merged measurements data.
2. **Measurement Summary**: A `.txt` (or `.csv`) file (`measurements_summary_{timestamp}.txt`) summarizing the measurements per day for each patient.

### Example Outputs

- **Merged Data CSV**:

| Patient Name     | Patient ID | Sex   | Index | Reason | Sys | Dia | HR  | Mean | Hour | Minute | Month | Day | Year | Tag | Comments | Collection Stage  |
|------------------|------------|-------|-------|--------|-----|-----|-----|------|------|--------|-------|-----|------|-----|----------|-------------------|
| Almustafa Qusai  | 00168743   | M     | 1     | 0      | 120 | 80  | 75  | 92   | 14   | 30     | 10    | 11  | 2024 | 0   | --       | Edited Awake BP   |
| Bao Duo          | 00168744   | F     | 2     | 0      | 115 | 70  | 72  | 88   | 15   | 45     | 10    | 16  | 2024 | 1   | --       | Omitted Asleep BP |

- **Measurement Summary (TXT)**:

```
Almustafa Qusai, 00168743, Days: 2
date: 10/11/2024 : 4 measurements
date: 10/14/2024 : 3 measurements

Bao Duo, 00168744, Days: 2
date: 10/16/2024 : 4 measurements
date: 10/19/2024 : 3 measurements
```

## Script Components

### `process_and_merge_asc_files_in_folder(folder_path)`
This is the main function of the script. It:
- Reads all `.asc` files in the specified folder and its subdirectories.
- Processes each file to extract patient data and measurement details.
- Merges the processed data into a single CSV file.
- Calls the `list_patient_measurements()` function to summarize patient measurements.

### `process_asc_file_with_stages_and_all_indices(asc_data)`
This function processes an individual `.asc` file:
- Extracts patient information and measurement data.
- Assigns a collection stage to each index.
- Returns a cleaned DataFrame ready for merging.

### `list_patient_measurements(df, output_measurements_file)`
This function summarizes patient measurements:
- Groups measurements by patient and date.
- Outputs the measurement summary to both the console and a file.

## Customization

- **Output Formats**: You can choose to save the measurement summary as either `.txt` or `.csv` by changing the file extension in the `output_measurements_file` variable.
- **Folder Path**: You can change the folder path to process different sets of `.asc` files.

## Notes

- Ensure that your `.asc` files have the correct format, including patient information and measurement data, as expected by the script.
- The script assumes that `.asc` files contain headers and specific columns like `Patient Name`, `Sys`, `Dia`, `HR`, etc.
```
