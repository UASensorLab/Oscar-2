# Let's create the README.md file with the content and save it for user to download.

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
