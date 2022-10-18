import fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy import orm
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from token_jwt import verify_token, JWT_SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     return verify_token(token, credentials_exception)


async def get_current_user(db: orm.Session = fastapi.Depends(get_db), token: str = fastapi.Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])

    except:
        raise fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )
    return schemas.User.from_orm(user)

