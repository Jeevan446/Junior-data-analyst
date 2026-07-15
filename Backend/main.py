from fastapi import FastAPI
from dotenv import load_dotenv
from routes.users import router as user_router
load_dotenv()
app=FastAPI()

app.include_router(user_router)
































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