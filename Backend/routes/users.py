from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
import random
import string
from database.queries import search_user,add_users
from core.files_to_dataframes1 import file_to_df

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


class Usermetadata(BaseModel):
    id:str
   
        
@router.post('/analyze')
def analyze(usermetadata:Usermetadata):
    try:
        is_user=search_user(usermetadata.id)
        if not is_user:
            raise HTTPException(status_code=404,detail="Please add some files first")
        file_to_df(usermetadata.id)
        return {"sucess":True,"message":"User files found sucessfully"}
        
        
    except HTTPException:
        raise
    except Exception as e:
        print("Error while analyzing data",e)
        raise HTTPException(status_code=500,detail="Internal server error while analyzing")

   

   
    


# @router.get('/users')
# def users():
#  return {'message':"Hello from users"}

