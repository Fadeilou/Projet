from typing import List

import fastapi
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import database
import oauth2
import schemas
from repository import historicales

router = APIRouter(
    prefix="/historical",
    tags=['Historicales']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowHistorical])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return historicales.get_all(db)


@router.get('/', response_model=List[schemas.ShowHistorical])
def all_by_user(db: Session = Depends(get_db), current_user: schemas.User = fastapi.Depends(oauth2.get_current_user)):
    current_user_id = current_user.id
    return historicales.get_all_by_user(current_user_id, db)


# @router.get('/', response_model=List[schemas.ShowHistorical])
# def get_all_by_user_and_analyse(db: Session = Depends(get_db), current_user: schemas.User = fastapi.Depends(oauth2.get_current_user)):
#     current_user_id = current_user.id
#     return historicales.get_all_by_user_and_analyse(current_user_id, db)



# @router.post('/', status_code=status.HTTP_201_CREATED, )
# def create(request: schemas.Historical, db: Session = Depends(get_db),
#            current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return historicales.create(request, db)


# @router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return historicales.destroy(id, db)


# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update(id: int, request: schemas.Historical, db: Session = Depends(get_db),
#            current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return historicales.update(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowHistorical)
def show(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return historicales.show(id, db)
