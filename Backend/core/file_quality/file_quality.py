from fastapi import HTTPException
import json
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
            # print(df_dict)
            missing_series=(df_dict["dataframe"].isna().sum())
            shape=(df_dict["dataframe"].shape)
            self.missing_arr.append({"Tablename":df_dict['name']})
            for index,value in missing_series.items():
                missing_dict={}
                missing_dict["column_name"]=index
                missing_dict["no_of_missing"]=int(value)
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
            # print(self.sending_arr)
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
            json_response=fetch_unique_columns(sending_dict)
            json_response = json_response.replace("```json", "").replace("```", "").strip()
            response_dict=json.loads(json_response)
            unique_column_list=response_dict["unique_columns"]
            # print(self.sending_arr)
            # print(unique_column_list)
            unique_column_arr=[]
            unique_column_dictonary={}
            for unique_column in unique_column_list:

                duplicated = self.df_dict["dataframe"][unique_column].duplicated()
                no_of_duplicated_value = int(duplicated.sum())
                total_values =int(self.df_dict["dataframe"][unique_column].count())
                unique_column_dictonary = {}
                unique_column_dictonary["column_name"] = unique_column
                unique_column_dictonary["no_of_duplicated_value"] = int(no_of_duplicated_value)
                unique_column_dictonary["duplicated_percentage"] = (
               float((no_of_duplicated_value / total_values) * 100)
                if total_values > 0 else 0
            )
                unique_column_arr.append(unique_column_dictonary)
    
            self.sending_arr.append(unique_column_arr)
            # print(type(self.sending_arr))
            # print(self.sending_arr)


        except Exception as e:
            print("Error while checking column values uniqueness",e)
            raise HTTPException(status_code=500,detail="Error while checking uniqueness of data")