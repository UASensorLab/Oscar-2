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
How It Works
Processing .asc Files:

The script reads .asc files from a specified folder.
It extracts patient information (name, ID, sex), measurement data (such as systolic, diastolic pressure), and assigns a collection stage (e.g., Edited Awake BP).
The files are merged into a single CSV file.
Summarizing Measurements:

After merging the data, the script groups the measurements by patient and date, calculating the number of measurements per day.
The summary also includes the number of unique days each patient was measured.
Folder Structure
ASC Files: Store all your .asc files in one folder.
Output: The script outputs two files:
A CSV with the merged measurement data.
A file with the measurement summary (can be .txt or .csv).
Usage
1. Modify the Folder Path
In the script, you need to specify the folder path where your .asc files are stored. Replace the path in the folder_path variable:
