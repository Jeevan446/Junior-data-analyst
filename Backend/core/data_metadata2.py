import pandas as pd
# from .files_to_dataframes1 import file_to_df
from .data_qualitycheck3 import check_data_quality

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
        dtype_extraction(df_arr)
        
    except Exception as e:
        print("Error while extracting data columns",e)

def dtype_extraction(df_arr):
    try:
        for df_dict in df_arr:
            df_dict['datatypes']=df_dict['dataframe'].dtypes.to_dict()
        shapeExtraction(df_arr)
    except Exception as e:
        print('Error while extracting datatypes of columns of dataframes')


def shapeExtraction(df_arr):
    try:
        for df_dict in df_arr:
            df_dict['shape']=df_dict['dataframe'].shape
            random_row(df_arr)
    except Exception as e:
        print("Eroor while extracting shape of dataframe",e)

def random_row(df_arr):
    try:
        for df_dict in df_arr:
            df_dict['random_data']=df_dict['dataframe'].sample().to_dict()
        # print(df_arr)
        check_data_quality(df_arr)
    except Exception as e:
        print("Error while extracting random row ",e)
