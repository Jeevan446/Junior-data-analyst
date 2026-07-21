from fastapi import FastAPI
from dotenv import load_dotenv
from routes.users import router as user_router
from routes.upload import router as upload_router
from database.queries import create_file_table
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
load_dotenv()

# create_file_table()
app.include_router(user_router)
app.include_router(upload_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)































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