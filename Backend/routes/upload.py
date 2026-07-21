from fastapi import APIRouter,Form,UploadFile,HTTPException
from database.queries import add_files,search_user,fetch_filenames
from outputs.clean_filename import clean_filename
from database.queries import is_file_exists
from pathlib import Path
from typing import List
router=APIRouter()

@router.post('/uploadfiles')
async def uploadfiles(files:List[UploadFile],user_id:str=Form()):

    try:
        valid_user=search_user(user_id)
        if not valid_user:
            raise HTTPException(status_code=404,detail="User not found")  
        
        for file in files:
            cleaned_file_name=clean_filename(file.filename)
            filename=user_id+'&'+cleaned_file_name
            
            file_exists=is_file_exists(user_id,filename)
            if file_exists:
                raise HTTPException(status_code=409,detail=f"{file.filename} already exists in db donot select it")
            path=Path('temp_files')/filename
            if(path.suffix!='.csv' and  path.suffix!='.xlsx' and path.suffix!='.xls'):
                raise HTTPException(status_code=415,detail="Unsupported file format")
            path.write_bytes(await file.read())

            add_files(filename,user_id)
        return{"sucess":True,"message":"file uploaded sucessfully"}

    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500,detail="Internal Server Error while uploading files")
    


@router.get('/uploadedfiles/{user_id}')
def uploadedfiles(user_id):
    try:
        filenames=fetch_filenames(user_id)
        filenamearr=[]
        for filename in filenames:
            file=Path(filename[0])
            filename=(file.stem.split('&')[1]+file.suffix)
            filenamearr.append(filename)
        return{'sucess':True,'filenames':filenamearr}
            
    except Exception as e:
        raise HTTPException(status_code=500,detail='Internal Server Error!')

