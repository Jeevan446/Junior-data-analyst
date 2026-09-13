import pandas as pd
from pathlib import Path
from .file_quality import call_quality
from fastapi import HTTPException
def file_to_df(file_name,user_id):
    try:
        # print(file_name_arr)
        dfs=[]


        path=Path(file_name)
        folder_file_path=Path("temp_files")/file_name
        df_name=path.stem.split("&")[1]

        if path.suffix==".csv":
            df=pd.read_csv(folder_file_path)

        elif path.suffix == ".xlsx":
            df = pd.read_excel(folder_file_path, engine="openpyxl")

        elif path.suffix == ".xls":
            df = pd.read_excel(folder_file_path, engine="xlrd")

        else:
            raise HTTPException(status_code=400,detail="Invalid file format")
 
        df_obj={
                "name":df_name,
                "dataframe":df
            }
        dfs.append(df_obj)

        return dfs
   
    except HTTPException:
        raise    

    except Exception as e:
        print("Error while converting files to dataframes",e)
        raise HTTPException(status_code=300,detail='dfdsfd')