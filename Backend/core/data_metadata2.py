import pandas as pd
# from .files_to_dataframes1 import file_to_df

def metadata_extraction(df_arr):
    try:
        # print(df_dict['imdb_top_1000'])
        columns_extraction(df_arr)
    except Exception as e:
        print("Error while metadata extracting",e)


def columns_extraction(df_arr):
    
    try:
        for df_dict in df_arr:
            #.columns returns pandas object of columns but tolist method converts the object to python list
            df_dict['columns']=df_dict["dataframe"].columns.tolist()
        print(df_arr)
    except Exception as e:
        print("Error while extracting data columns",e)