from fastapi import HTTPException
import json
from datetime import datetime
from dateutil import parser
import pandas as pd
import re
def call_quality(dfs):
    for df_dict in dfs:
        c=Uniqueness(df_dict)
        
class Completeness:
    def __init__(self,df_dict):
        self.df_dict=df_dict
        self.sending_arr=[]
        self.missing_values()
    def missing_values(self):
        try:
            missing_series=self.df_dict['dataframe'].isna().sum()
            for index,value in missing_series.items():
                dict={}
                dict['column_name']=index
                rows=self.df_dict['dataframe'][index].shape[0]
                dict['no_of_missing_values']=int(value)
                dict['missing_percentage']=float(value/rows)*100
                dict['datatype']=str(self.df_dict['dataframe'][index].dtype)
                self.sending_arr.append(dict)   
            
        except Exception as e:
            print("Error while checking completeness of data",e)
            raise HTTPException(status_code=500,detail="Error while checking completeness of data")
    def send_values(self):
        return self.sending_arr

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
            self.uniqueness_column()
        except Exception as e:
            print("Error while checking duplicated rows uniqueness",e)
            raise HTTPException(status_code=500,detail="Error while checking uniqueness of data")
    
    def uniqueness_column(self):
        u_array=[]
        try:
            df=self.df_dict['dataframe']
            for column_name in df.columns:
                u_dict={}
                u_dict['column_name']=column_name
                u_dict['datatype']=str(df[column_name].dtype)
                u_dict['no_of_duplicated']=int(df[column_name].duplicated().sum())
                u_dict['duplicate_percentage']=float((df[column_name].duplicated().sum())/(df[column_name].shape[0]))*100
                u_array.append(u_dict)
            self.sending_arr.append(u_array)

        except Exception as e:
            print("Error while checking uniqueness of columns",e)
            raise HTTPException(status_code=500,detail="Error while checking uniqueness of data")
    def send_values(self):
        return self.sending_arr



class Validation():
    def __init__(self,dataframe_dict,column_name,validation_type,validation_metadata):
        self.df_dict=dataframe_dict
        self.column_name=column_name
        self.validation_type=validation_type
        self.validation_metadata=validation_metadata
        self.sending_arr=[]
        self.function_call()
    def function_call(self):
        if(self.validation_type=="Date"):
            self.check_for_date()
        elif(self.validation_type=='Email'):
            self.email_validation()
    def check_for_date(self):
        try:
            if(self.validation_metadata['mixed']==True):
                def cd(date):
                    if pd.isna(date):
                        return "miss" 
                    date=str(date)
                    try:
                        parser.parse(date, dayfirst=False)
                        return True
                    except:
                        try:
                            parser.parse(date, dayfirst=True)
                            return True
                        except:
                            return False
                validate_date_series=self.df_dict['dataframe'][self.column_name].apply(cd)
                no_of_invalid=validate_date_series.value_counts().get(False, 0)
                no_of_missing=validate_date_series.value_counts().get('miss', 0)
                s_dict={}
                s_dict['column_name']=self.column_name
                s_dict['no_of_invalid']=int(no_of_invalid)
                s_dict['invalid_percentage']=float((no_of_invalid/self.df_dict['dataframe'][self.column_name].shape[0])*100)
                s_dict['no_of_missing']=int(no_of_missing)
                s_dict['missing_percentage']=float((no_of_missing/self.df_dict['dataframe'][self.column_name].shape[0])*100)
                self.sending_arr=s_dict
                self.send_values()

                         
            else:
                def cd(date):
                    if pd.isna(date):
                        return "miss"
                    try:
                        (datetime.strptime(str(date), self.validation_metadata['pattern']))
                        return True
                    except:
                        return False

                validate_date_series = self.df_dict['dataframe'][self.column_name].apply(cd)
                print(validate_date_series)
                no_of_invalid = validate_date_series.value_counts().get(False, 0)
                no_of_missing = validate_date_series.value_counts().get('miss', 0)

                total_rows = len(validate_date_series)

                s_dict = {
        'column_name': self.column_name,
        'no_of_invalid': int(no_of_invalid),
        'invalid_percentage': float(no_of_invalid / total_rows * 100) if total_rows else 0.0,
        'no_of_missing': int(no_of_missing),
        'missing_percentage': float(no_of_missing / total_rows * 100) if total_rows else 0.0
                }

                self.sending_arr = s_dict
                self.send_values()

        except Exception as e:
            print("Error while checking date validation",e)
            raise HTTPException(status_code=500,detail="Error while checking validity of data")
    def email_validation(self):
        try:
            def validate_email(email):
                if pd.isna(email):
                    return "miss"
                email=str(email)
                pattern= '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                email_object=re.fullmatch(pattern,email) #returns Null if donot matches the pattern if matches returns object
                if email_object:
                    return True
                else:
                    return False



            email_column=self.df_dict['dataframe'][self.column_name]
            Validation_series=email_column.apply(validate_email)
            validation_count=(Validation_series.value_counts())
            total_rows=self.df_dict['dataframe'][self.column_name].shape[0]
            no_of_invalid=int(validation_count[False])
            invalid_percentage=float((no_of_invalid/total_rows)*100)
            no_of_missing=int(validation_count['miss'])
            missing_percentage=float((no_of_missing/total_rows)*100)
            s_dict={
                "column_name":self.column_name,
                "no_of_invalid":no_of_invalid,
                "invalid_percentage":invalid_percentage,
                "no_of_missing":no_of_missing,
                "missing_percentage":missing_percentage
            }
            self.sending_arr.append(s_dict)
            self.send_values()
        except Exception as e:
            print("Error while checking validation",e)
            raise HTTPException(status_code=500,detail='Error while checking validity of data')

    def send_values(self):
        return self.sending_arr
