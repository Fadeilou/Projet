from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models


def get_all(db: Session):
    historicales = db.query(models.Historical).all()
    return historicales


def get_all_by_user(idUser: int, db: Session):
    historicales = db.query(models.Historical).filter(models.Historical.idUser == idUser).all()
    return historicales


def get_all_by_user_and_analyse(idUser: int, idAnalysisResult: int, db: Session):
    historicales = db.query(models.Historical).filter(models.Historical.idUser == idUser,
                                                      models.Historical.idAnalysisResult == idAnalysisResult).first()
    return historicales


def show(id: int, db: Session):
    historical = db.query(models.Historical).filter(models.Historical.id == id).first()
    if not historical:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile with the id {id} is not available")
    return historical


def create(idUser, idAnalysisResult, db: Session):
    new_historical = models.Historical(idAnalysisResult=idAnalysisResult, idUser=idUser)
    db.add(new_historical)
    db.commit()
    db.refresh(new_historical)
    return new_historical
