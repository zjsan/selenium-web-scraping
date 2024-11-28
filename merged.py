#Python program to merge downloaded excel files into a single file

# Directory where files are saved
import pandas as pd
import numpy as np
import os

directory = r'C:\Users\YourName\Documents\SDG Datas\Scraping'

# List all Excel files in the directory
excel_files = [f for f in os.listdir(directory) if f.endswith('.xlsx')]

# Initialize an empty DataFrame
merged_data = pd.DataFrame()

# Loop through each file and append its content
for file in excel_files:
    file_path = os.path.join(directory, file)
    data = pd.read_excel(file_path)
    merged_data = pd.concat([merged_data, data], ignore_index=True)

# Save the merged file
merged_file_path = os.path.join(directory, 'Merged_Universities_Data.xlsx')
merged_data.to_excel(merged_file_path, index=False)

print(f"Merged file saved at: {merged_file_path}")