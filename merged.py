#Python program to merge downloaded excel files into a single file and individual sheets

import pandas as pd
import os

try:
    # Define the directory containing the Excel files
    directory = r'C:\Users\User\Documents\SDG Datas\Scraping'

    # List all Excel files in the directory
    excel_files = [f for f in os.listdir(directory) if f.endswith('.xlsx')]

    # Check if Excel files exist
    if not excel_files:
        raise FileNotFoundError("No Excel files found in the directory.")

    # Define sheets of interest
    xls = ['SDG Overall', 'Metric Scores', 'Indicator Scores']

    # Dictionary to store data for each sheet
    sheet_data = {sheet: pd.DataFrame() for sheet in xls}

    print("--- Available Excel files: ---")
    print(excel_files)
    print("\n")

    for file in excel_files:
        file_path = os.path.join(directory, file)
        worksheets = pd.ExcelFile(file_path)  # Load Excel file
        sheets = worksheets.sheet_names

        print(f"Processing file: {file} with sheets: {sheets}")

        # Iterate through the sheets in the current file
        for sheet in sheets:
            if sheet in xls:  # Check if the sheet is in the target list
                print(f"Reading sheet: {sheet} from file: {file}")
                data = pd.read_excel(file_path, sheet_name=sheet)
                sheet_data[sheet] = pd.concat([sheet_data[sheet], data], ignore_index=True)

    # Save the data to a single Excel file with individual sheets
    merged_file_path = os.path.join(directory, 'Merged_Universities_Data3.xlsx')
    with pd.ExcelWriter(merged_file_path, engine='openpyxl') as writer:
        for sheet, data in sheet_data.items():
            data.to_excel(writer, sheet_name=sheet, index=False)

    print("\nSuccess! Merged file saved at:")
    print(merged_file_path)

except Exception as e:
    print(f"Error: {e}")
    print("---- Excel files could not be merged ----")
