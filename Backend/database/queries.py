from .connection import db_connect   
import psycopg
import json 
 
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

def is_file_exists(user_id,filename):
    try:
        conn=None
        cursor=None
        conn=db_connect()
        cursor=conn.cursor()
        cursor.execute('''
        SELECT* FROM file WHERE filename=%s AND user_id=%s 
        ''',(filename,user_id))
        files=cursor.fetchall()
        return files

    except Exception as e:
        print("Error while searching file",e)
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def add_files(filename,userid):
    try:
        conn=None
        cursor=None
        conn=db_connect()
        cursor=conn.cursor()
        cursor.execute('''
        INSERT INTO file(filename,user_id)
        VALUES(%s,%s)
        ''',(filename,userid))
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print("Error while adding file in filetable",e)
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_filenames(user_id):
    try:
        conn=None
        cursor=None
        conn=db_connect()
        cursor=conn.cursor()
        cursor.execute('''
        SELECT filename FROM file
        WHERE user_id=%s
        
        ''',(user_id,))
        data=cursor.fetchall()
        return data
    except Exception as e:
        print("Error while fetching filenames from userid",e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def create_quality_table():
    try:
        conn=None
        cursor=None
        conn=db_connect()
        cursor=conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS quality(
         user_id VARCHAR REFERENCES users(user_id),
         quality_id VARCHAR,
         filename VARCHAR ,
         missing_values JSONB,
         empty_strings JSONB,
         duplicate_rows JSONB

        )
        ''')
        conn.commit()

    except Exception as e:
        print("Error while creating quality table",e)
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def file_qualityid_exists(quality_id):
    try:
        conn=None
        cursor=None
        conn=db_connect()
        cursor=conn.cursor()
        cursor.execute('''
        SELECT* FROM quality
        WHERE quality_id=%s
        ''',(quality_id,))
        data=cursor.fetchone()
        return data
    except Exception as e:
        print("Error while checking quality id")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def add_file_quality_info(user_id,quality_id,quality_arr):
    try:
        conn=None
        cursor=None
        conn=db_connect()
        cursor=conn.cursor()
        for single_data_quality in quality_arr:
            cursor.execute('''
            INSERT INTO quality(user_id,quality_id,filename,missing_values,empty_strings,duplicate_rows)
            VALUES(%s,%s,%s,%s,%s,%s)
            
            ''',(user_id,quality_id,single_data_quality['filename'],json.dumps(single_data_quality['Missing values']),json.dumps(single_data_quality['Empty strings']),json.dumps(single_data_quality['duplicate rows']))
            )
            conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print("Error while adding file quality information")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
def get_all_files_quality(quality_id):
    try:
        conn=None
        cursor=None
        conn=db_connect()
        cursor=conn.cursor()
        cursor.execute('''
        SELECT* From quality
        WHERE quality_id=%s
        ''',(quality_id,))
        data=cursor.fetchall()
    except Exception as e:
        print("Error while getting all file quality")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            