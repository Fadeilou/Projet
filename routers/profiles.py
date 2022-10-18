from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import database
import oauth2
import schemas
from repository import profiles

router = APIRouter(
    prefix="/profile",
    tags=['profiles']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowProfile])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profiles.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED, )
def create(request: schemas.Profile, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profiles.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profiles.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Profile, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profiles.update(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowProfile)
def show(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return profiles.show(id, db)
