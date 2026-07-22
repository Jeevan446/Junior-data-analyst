import pandas as pd
from .data_metadata2 import metadata_extraction
from pathlib import Path

def file_to_df(file_name_arr,user_id):
    try:
        # print(file_name_arr)
        dfs=[]

        for file_path in file_name_arr:
            path=Path(file_path)
            folder_file_path=Path("temp_files")/file_path
            df_name=path.stem.split("&")[1]

            if path.suffix==".csv":
                df=pd.read_csv(folder_file_path)

            elif path.suffix in [".xlsx",".xls"]:
                df=pd.read_excel(folder_file_path)

            else:
                continue

            df_obj={
                "name":df_name,
                "dataframe":df
            }
            dfs.append(df_obj)

        # print(dfs)
        metadata_extraction(dfs)

    except Exception as e:
        print("Error while converting files to dataframes",e)