import os
from fastapi import HTTPException
import psycopg

key=os.getenv('DB_URI')
def db_connect():
    try:
        conn=psycopg.connect(key)
        return conn
    except Exception as e:
        print("Error while connecting to db",e)
    
