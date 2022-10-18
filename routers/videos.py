from typing import List
import shutil
import fastapi
from datetime import datetime
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import database
import models
import oauth2
import schemas
from repository import videos

router = APIRouter(
    prefix="/video",
    tags=['videos']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowVideo])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return videos.get_all(db)


@router.get('/', response_model=schemas.User)
def all_by_user(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return current_user


@router.get("/api/users/me", response_model=schemas.User)
async def get_user(user: schemas.User = fastapi.Depends(oauth2.get_current_user)):
    return user


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Video, current_user: schemas.User = fastapi.Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    return videos.create(request, current_user.id, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return videos.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Video, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    return videos.update(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowVideo)
def show(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return videos.show(id, db)


@router.post('/upload_model', status_code=status.HTTP_201_CREATED)
def upload_model(file: UploadFile = File(...)):
    print("filename = ", file.filename)  # getting filename
    destination_file_path = "ml_models/" + file.filename  # location to store file
    with open(f'{destination_file_path}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_name": file.filename}


@router.post('/upload_video', status_code=status.HTTP_201_CREATED)
def upload_model(file: UploadFile = File(...)):
    print("filename = ", file.filename)  # getting filename
    destination_file_path = "public/" + file.filename  # location to store file
    with open(f'{destination_file_path}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_name": file.filename}
