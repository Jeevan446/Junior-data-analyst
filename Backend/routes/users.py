from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
import random
import string
from database.queries import search_user,add_users
from core.file_quality.files_to_dataframes1 import file_to_df
from outputs.clean_filename import clean_filename
from typing import List
from core.file_quality.file_quality import Completeness,Uniqueness
from llm.Completeness import completeness_llm

router=APIRouter()


def randomstring():
    result = ""
    for i in range(10):
        result += random.choice(string.ascii_letters)
    return result






class User(BaseModel):
    company_type:str
    company_description:str



@router.post('/createuser')
def create_new_user(user:User):
    try:
        if(user.company_type):
            while True:
                random_str = randomstring()
                new_user_id = user.company_type+ random_str
                data = search_user(new_user_id)
                if not data:
                    break
                 
        else:
            while True:
                random_str = randomstring()
                new_user_id = random_str
                data = search_user(new_user_id)
                if not data:
                     break 
             
        add_users(new_user_id,user.company_type,user.company_description)
        return{"sucess":True,"message":"User created sucessfully","user":{
            "user_id":new_user_id
        }}

    except Exception as e:
        print("Error while creating a user",e)
        raise HTTPException(status_code=500,detail="Internal Server Error While creating user")



class User(BaseModel):
    user_id: str
    filenames: List[str]
           
@router.post('/user/file/qualitycheck')
def analyze(user: User):
    try:
        is_user = search_user(user.user_id)

        if not is_user:
            raise HTTPException(
                status_code=404,
                detail="Please add some files first"
            )

        arr = []
      
        for filename in user.filenames:

            cleaned_file_name = clean_filename(filename)

            combined_filename = (
                user.user_id + '&' + cleaned_file_name
            )

            arr.append(combined_filename)
       
        # print (d)
        return {
            "success": True,
            "message": "User files found successfully",
            "file_arr":arr
        }

    except HTTPException:
        raise
    except Exception as e:
        print("Error while analyzing data", e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while analyzing"
        )
   

class data_completeness(BaseModel):
    user_id:str

@router.post('/user/file/qualitycheck/completeness/{filename}')
def check_data_completeness(filename,user:data_completeness):
    try:
        dataframe=file_to_df(filename,user.user_id)
        print(dataframe)
        c=Completeness(dataframe[0])
        print(c.sending_values())
        llm_feed=(c.sending_values())
        llm_response=completeness_llm(llm_feed)
        return {'sucess':True,'llm_response':{"message":llm_response}}

    except Exception as e:
        print("Error during checking completenss of data",e)
        raise HTTPException(status_code=500,detail="Error during quality check of data")


class data_uniqueness(BaseModel):
    user_id:str
    table_type:str

@router.post('/user/file/qualitycheck/uniqueness/{filename}')
def check_data_uniqueness(uniqueness:data_uniqueness,filename):
    try:
        dataframe_arr=file_to_df(filename,uniqueness.user_id)
        u=Uniqueness(dataframe_arr[0],uniqueness.table_type)
        
    except Exception as e:
        print("Error during checking uniqueness of data",e)
        raise HTTPException(status_code=500,detail="Error during quality check of data")

