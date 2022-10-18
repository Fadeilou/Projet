from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import database
import oauth2
import schemas
from repository import users

router = APIRouter(
    prefix="/user",
    tags=['users']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowUser])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return users.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED, )
def create(request: schemas.CreateUser, db: Session = Depends(get_db)):
    return users.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return users.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.User, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    return users.update(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def show(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return users.show(id, db)
