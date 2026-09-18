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
            print("Error while checking missing values completeness",e)
            raise HTTPException(status_code=500,
            detail="Error while checking completeness of data")

    def sending_values(self):
        m=self.missing_arr
        return m

        

class Uniqueness():
    def __init__(self,df_dict):
        self.df_dict=df_dict
        self.sending_arr=[]
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
        except Exception as e:
            print("Error while checking duplicated rows uniqueness",e)
            raise HTTPException(status_code=500,detail="Error while check uniqueness of data")