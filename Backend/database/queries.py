from .connection import db_connect   
import psycopg

 
# create user table
def user_table():
    try:
        conn=None
        cursor=None
        conn=db_connect()
        cursor=conn.cursor()
        cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
                     user_id VARCHAR(60) PRIMARY KEY,
                       company_type VARCHAR(60),
                       company_description VARCHAR(1000)
                       )
                        ''')
        conn.commit()
    except Exception as e:
        print("Error while creating user table",e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
        
        
        
# adding users to the users table
def add_users(user_id,company_type=None,company_description=None):
    try:
        conn=None
        cursor=None
        conn=db_connect()
        cursor=conn.cursor()
        cursor .execute('''
        INSERT INTO users(user_id,company_type,company_description)
        VALUES(%s,%s,%s)
        ''',(user_id,company_type,company_description))
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
            print("Error while adding users in user table",e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




# searching in user table that the id exists or not
def search_user(user_id):
    try:
        conn=None
        cursor=None
        conn=db_connect()
        cursor=conn.cursor()
        cursor.execute('''
        SELECT user_id FROM users WHERE user_id=%s
        ''',(user_id,))
        data=cursor.fetchone()
        return data
    except Exception as e:
        print("Error while searching for users",e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




# create file table 
def create_file_table():
    try:
        conn=None
        cursor=None
        conn=db_connect()
        cursor=conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS file(
        filename VARCHAR PRIMARY KEY,
        user_id VARCHAR REFERENCES users(user_id)
    )
    ''')
        conn.commit()
    except Exception as e:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Error while creating file table",e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

   

  



        
    

