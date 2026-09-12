import pandas as pd
from pathlib import Path
from .file_quality import call_quality
from fastapi import HTTPException
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

            elif path.suffix == ".xlsx":
                df = pd.read_excel(folder_file_path, engine="openpyxl")

            elif path.suffix == ".xls":
                df = pd.read_excel(folder_file_path, engine="xlrd")

            else:
                continue

            df_obj={
                "name":df_name,
                "dataframe":df
            }
            dfs.append(df_obj)

        call_quality(dfs)
   
    except HTTPException:
        raise    

    except Exception as e:
        print("Error while converting files to dataframes",e)
        raise HTTPException(status_code=300,detail='dfdsfd')