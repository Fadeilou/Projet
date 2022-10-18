from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas


def get_all(db: Session):
    profiles = db.query(models.Profile).all()
    return profiles


def create(request: schemas.Profile, db: Session):
    new_profile = models.Profile(fullname=request.fullname, pathProfile=request.pathProfile, idUser=1)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


def destroy(id: int, db: Session):
    profile = db.query(models.Profile).filter(models.Profile.id == id)

    if not profile.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile with id {id} not found")

    profile.delete(synchronize_session=False)
    db.commit()
    return 'done'


def update(id: int, request: schemas.Profile, db: Session):
    profile = db.query(models.Profile).filter(models.Profile.id == id)

    if not profile.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile with id {id} not found")

    profile.update(request)
    db.commit()
    return 'updated'


def show(id: int, db: Session):
    profile = db.query(models.Profile).filter(models.Profile.id == id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile with the id {id} is not available")
    return profile
