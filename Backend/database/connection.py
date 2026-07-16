import os
from fastapi import HTTPException
import psycopg
from dotenv import load_dotenv
load_dotenv()

key=os.getenv('DB_URI')
print(key)
def db_connect():
    try:
        conn=psycopg.connect(key)
        return conn
    except Exception as e:
        print("Error while connecting to db",e)
    
