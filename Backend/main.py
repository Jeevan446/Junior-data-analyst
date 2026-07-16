from fastapi import FastAPI
from dotenv import load_dotenv
from routes.users import router as user_router
from routes.upload import router as upload_router
from database.queries import create_file_table
load_dotenv()
app=FastAPI()

create_file_table()
app.include_router(user_router)
app.include_router(upload_router)
































# from database.queries import user_table
# user_table()
 
# from database.queries import add_users
# add_users("Namea","HEllo","WOrld")



from database.queries import search_user
user=search_user('Nameas')
# print(user)

if user:
    print('User found')
else:
    print("User not found")