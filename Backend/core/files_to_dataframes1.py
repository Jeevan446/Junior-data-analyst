import pandas as pd
from database.queries import fetch_filenames
from pathlib import Path
def file_to_df(user_id):
    try:
        file_paths=fetch_filenames(user_id)
        dfs={}
        for file_path in file_paths:
            path=Path(file_path[0])
            if(path.suffix=='.xslx' or path.suffix=='.xls'):
                folder_file_path='temp_files/'+file_path[0]
                df_name = path.stem.split("&")[1]
                dfs[df_name] = pd.read_excel(folder_file_path)
            else:
                folder_file_path='temp_files/'+file_path[0]
                df_name=path.stem.split("&")[1]
                dfs[df_name] = pd.read_csv(folder_file_path)
        
        print(dfs['imdb_top_1000'])
    except Exception as e:
        print("Error while converting files to dataframes",e)

        
    
    





    #     print(file[0])
    #     if 
    # return files


