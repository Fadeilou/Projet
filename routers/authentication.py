from http.client import HTTPException

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database
import models
import schemas
from hashing import Hash
from token_jwt import create_access_token

router = APIRouter(tags=['authentication'])


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Invalid Credentials")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Incorrect password")
    # generate a jwt token

    access_token = create_access_token(
        data={"email": user.email,
              "id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}
