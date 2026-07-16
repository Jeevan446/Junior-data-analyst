from fastapi import APIRouter,Form,UploadFile,HTTPException
from database.queries import add_files
from pathlib import Path
from typing import List
router=APIRouter()

@router.post('/uploadfiles')
async def uploadfiles(files:List[UploadFile],user_id:str=Form()):

    try:
        for file in files:
            filename=user_id+'&'+file.filename
            path=Path('temp_files')/filename
            path.write_bytes(await file.read())
            add_files(filename,user_id)
        return{"sucess":True,"message":"file uploaded sucessfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail="Internal Server Error while uploading files")
    