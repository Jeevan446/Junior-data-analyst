from fastapi import HTTPException
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
            print("Error which checking missing values completeness",e)
            raise HTTPException(status_code=500,
            detail="Error while checking completeness of data")

    def sending_values(self):
        m=self.missing_arr
        return m

        

# class Uniqueness(Completeness):
#     def __init__(self,df_dict):
#         super().__init__(df_dict)
#         self.df_dict=df_dict
#         self.duplicated_rows()
#     def duplicated_rows(self):
#         try:
#             duplicated_rows=self.df_dict['dataframe'].duplicated().sum()
#             duplicated_row_percentage=(duplicated_rows/self.df_dict['dataframe'].shape[0])*100  
#         except Exception as e:
#             print("Error while checking duplicated rows",e)
#             raise HTTPException(status_code=500,detail="Error while checking Uniqueness of data")
#     def unique_columns(self):
#         try:
#             print("Hello world")
#         except Exception as e:
#             print("Error while checking duplicated rows",e)
#             raise HTTPException(status_code=500,detail="Error while checking Uniqueness of data")
  








    
    