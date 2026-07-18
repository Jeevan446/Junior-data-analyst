import pandas as pd
from database.queries import fetch_filenames
from .data_metadata2 import metadata_extraction
from pathlib import Path
def file_to_df(user_id):
    try:
        file_paths=fetch_filenames(user_id)
        dfs=[]
        for file_path in file_paths:
            path=Path(file_path[0])
            if(path.suffix=='.xslx' or path.suffix=='.xls'):
                folder_file_path='temp_files/'+file_path[0]
                df_name = path.stem.split("&")[1]
                df_obj={
                    'name':df_name,
                    'dataframe': pd.read_csv(folder_file_path)
                }
                dfs.append(df_obj)
            else:
                folder_file_path='temp_files/'+file_path[0]
                df_name=path.stem.split("&")[1]
                df_obj={
                    'name':df_name,
                    'dataframe': pd.read_csv(folder_file_path)
                }
                dfs.append(df_obj)
                
        
        metadata_extraction(dfs)
    except Exception as e:
        print("Error while converting files to dataframes",e)

        
    
    





    #     print(file[0])
    #     if 
    # return files


