from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
import random
import string
from database.queries import search_user,add_users,file_qualityid_exists,add_file_quality_info,create_quality_table
from core.files_to_dataframes1 import file_to_df
from outputs.clean_filename import clean_filename
from typing import List

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
        create_quality_table()
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
        
        quality_arr=file_to_df(arr, user.user_id)


        while True:
            quality_id=randomstring()
            is_quality_id_exists=file_qualityid_exists(quality_id)
            if not is_quality_id_exists:
                break
        
        add_file_quality_info(user.user_id,quality_id,quality_arr)


       
        # print (d)
        return {
            "success": True,
            "message": "User files found successfully",
            "quality_id":quality_id
        }

    except HTTPException:
        raise
    except Exception as e:
        print("Error while analyzing data", e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while analyzing"
        )
   
    


# @router.get('/users')
# def users():
#  return {'message':"Hello from users"}

