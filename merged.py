#Python program to merge downloaded excel files into a single file

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
    
    
    xls = ['SDG Highlight','Metric Scores','Indicator Scores']
    
    #print(xls[0],xls[1],xls[2])
    
    # Loop through each file and append its content
    for file in excel_files:
        
        file_path = os.path.join(directory, file)#get excel file in excel_files
        worksheets = pd.ExcelFile(str(directory) + "/" + file)
        sheets = worksheets.sheet_names
        print(sheets)
       
        #iterate through the worksheets in the excel file
        for sheet in sheets:
            pointer = 0 
             
            if sheet == xls[0] or sheet == xls[1] or xls[2]:
            #iterate through xls to combine the selected sheets
                for specific_sheets in xls:
                        data = pd.read_excel(str(directory) + "/" + file,sheet_name = specific_sheets)#read sheet
                        print("\n", specific_sheets )
                        
                        if pointer == 3:
                            break
                        
                        if pointer > 1:
                            #pass 
                            print(pointer)
                            merged_data = pd.concat([merged_data, data], ignore_index=True)
                            #need logic to create new sheet
                            
                            with pd.ExcelWriter('Merged_Universities_Data3.xlsx', engine='openpyxl', mode='a') as writer:
                                # Write the new DataFrame to a new sheet
                                merged_data.to_excel(writer, sheet_name='New Sheet', index=False)
                            
                        else:
                            #pass
                            print(pointer)
                            # merged_data = pd.concat([merged_data, data], ignore_index=True)
                            # Save the merged file
                            #merged_file_path = os.path.join(directory, 'Merged_Universities_Data3.xlsx')
                            #merged_data.to_excel(merged_file_path, index=False)
                            
                        pointer += 1
                        
                        # Clear all contents of the DataFrame 
                        # merged_data.drop(merged_data.index, inplace=True)    
              
            if pointer == 3:
                break
                                 
            continue        
                
    print("\nsuccess displaying sheets")
    #print(f"Merged file saved at: {merged_file_path}")
    
except Exception as e:
    print(f"Error: {e}\n")
    print("----Excel files can't be merged----")
finally:
    # Saving changes and closing writer
    writer.save()
    writer.close()
