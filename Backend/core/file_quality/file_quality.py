from fastapi import HTTPException
from llm.Uniqueness import fetch_unique_columns
def call_quality(dfs):
    for df_dict in dfs:
        c=Uniqueness(df_dict)
        
class Completeness:
    def __init__(self,df_dict):
        self.df_dict=df_dict
        self.missing_arr=[]
        self.missing_values()
    def missing_values(self):
        try:
            df_dict=self.df_dict
            print(df_dict)
            missing_series=(df_dict["dataframe"].isna().sum())
            shape=(df_dict["dataframe"].shape)
            self.missing_arr.append({"Tablename":df_dict['name']})
            for index,value in missing_series.items():
                missing_dict={}
                missing_dict["column_name"]=index
                missing_dict["no_of_missing"]=value
                missing_dict['missing_percentage']=(value/(shape[0]))*100
                self.missing_arr.append(missing_dict)
            self.missing_arr.append({"Random_values":df_dict['random_data']})
        except Exception as e:
            print("Error while checking missing values completeness",e)
            raise HTTPException(status_code=500,
            detail="Error while checking completeness of data")

    def sending_values(self):
        m=self.missing_arr
        return m

        

class Uniqueness():
    def __init__(self,df_dict,table_type):
        self.df_dict=df_dict
        self.sending_arr=[]
        self.table_type=table_type
        self.duplicated_rows()
    def duplicated_rows(self):
        try:
            no_of_duplicated=self.df_dict['dataframe'].duplicated().sum()
            duplicated_percentage=(no_of_duplicated/self.df_dict['dataframe'].shape[0])*100
            duplicate_dict={}
            duplicate_dict['no_of_duplicated_rows']=int(no_of_duplicated)
            duplicate_dict['duplicated_rows_percenage']=float(duplicated_percentage)
            self.sending_arr.append(duplicate_dict)
            print(self.sending_arr)
            self.column_value_uniqueness()
        except Exception as e:
            print("Error while checking duplicated rows uniqueness",e)
            raise HTTPException(status_code=500,detail="Error while checking uniqueness of data")
    def column_value_uniqueness(self):
        try:
            sending_dict={}
            sending_dict["filename"]=self.df_dict['name']
            sending_dict["table_type"]=self.table_type
            sending_dict["column_names"]=self.df_dict['dataframe'].columns.to_list()
            print(sending_dict)
            fetch_unique_columns(sending_dict)
            
        except Exception as e:
            print("Error while checking column values uniqueness",e)
            raise HTTPException(status_code=500,detail="Error while checking uniqueness of data")