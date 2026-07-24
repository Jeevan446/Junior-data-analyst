def check_data_quality(df_arr):
    try:
        return check_missing_values(df_arr)
    except Exception as e:
        print("Error while cheking data quality")
        raise
      

def check_missing_values(df_arr):
    try:
        for df_dict in df_arr:
            missing_values=df_dict['dataframe'].isnull().sum().to_dict()
            data_quality={
            'Missing values':missing_values
            }
            df_dict['data_quality']=data_quality
        return check_empty_strings(df_arr)
    except Exception as e:
        print("Error while checking for missing values",e)
        raise
    
def check_empty_strings(df_arr):
    try:
        for df_dict in df_arr:
            empty_strings=(df_dict['dataframe'].astype(str).apply(lambda col: col.str.strip() == "").sum().to_dict())
            df_dict['data_quality']['Empty strings']=empty_strings
        return check_duplicated(df_arr)
    except Exception as e:
        print("Error while checking for missing values",e)
        raise


def check_duplicated(df_arr):
    try:
        for df_dict in df_arr:
            df_dict['data_quality']['duplicate columns']=int(df_dict['dataframe'].duplicated().sum())
        # print(df_arr)
        
         
        # sending data quality report for frontend
        sending_arr=[]
        for df_dict in df_arr:
            send_dict=df_dict['data_quality']
            sending_arr.append(send_dict)
        return(sending_arr)

    except Exception as e:
        print("Error while analyzing duplicated columns",e)
        raise

    

