def check_data_quality(df_arr):
    try:
        check_missing_values(df_arr)
    except Exception as e:
        print("Error while cheking data quality")
      

def check_missing_values(df_arr):
    try:
        for df_dict in df_arr:
            missing_values=df_dict['dataframe'].isnull().sum().to_dict()
            data_quality={
            'Missing values':missing_values
            }
            df_dict['data_quality']=data_quality
        check_empty_strings(df_arr)
        print(df_arr)
    except Exception as e:
        print("Error while checking for missing values",e)
    
def check_empty_strings(df_arr):
    try:
        for df_dict in df_arr:
            empty_strings=(df_dict['dataframe'].astype(str).apply(lambda col: col.str.strip() == "").sum().to_dict())
            df_dict['data_quality']['Empty strings']=empty_strings
        print(df_arr)
    except Exception as e:
        print("Error while checking for missing values",e)

    
