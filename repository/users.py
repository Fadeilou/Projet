from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from hashing import Hash


def get_all(db: Session):
    users = db.query(models.User).all()
    return users


def create(request: schemas.User, db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with this email already exist")

    new_user = models.User(username=request.username, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user


def destroy(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    user.delete(synchronize_session=False)
    db.commit()
    return 'done'


def update(id: int, request: schemas.User, db: Session):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    user.update(request)
    db.commit()
    return 'updated'
