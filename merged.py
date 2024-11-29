#Python program to merge downloaded excel files into a single file

# Directory where files are saved
import pandas as pd
import numpy as np
import os

try: 

    directory = r'C:\Users\User\Documents\SDG Datas\Scraping'

    # List all Excel files in the directory
    excel_files = [f for f in os.listdir(directory) if f.endswith('.xlsx')]

    # Initialize an empty DataFrame
    merged_data = pd.DataFrame()
    print("---Available excel files: ---",excel_files)
    print("\n")
    # Loop through each file and append its content
    for file in excel_files:
        #file_path = os.path.join(directory, file)#get excel file in excel_files
        worksheets = pd.ExcelFile(str(directory) + "/" + file)
        sheets = worksheets.sheet_names
        print(sheets)
        # if file.startswith("SDG Overall")
        # data = pd.read_excel(file_path)#read excel file
        # merged_data = pd.concat([merged_data, data], ignore_index=True)#store excel in the merged_data 
    print("\nsuccess displaying sheets")
    # # Save the merged file
    # merged_file_path = os.path.join(directory, 'Merged_Universities_Data.xlsx')
    # merged_data.to_excel(merged_file_path, index=False)

    # print(f"Merged file saved at: {merged_file_path}")
except Exception as e:
    print(f"Error: {e}\n")
    print("----Excel files can't be merged----")
