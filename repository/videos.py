from datetime import datetime
import shutil
from fastapi import HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import models
import schemas


def get_all(db: Session):
    videos = db.query(models.Video).all()
    return videos


def get_all_by_user(idUser: int, db: Session):
    videos = db.query(models.Video).filter(models.Video.idUser == idUser).all()
    return videos


def create(request: schemas.Video, user_id: int, db: Session):
    # print("filename = ", file.filename)
    # destination_file_path = "public/" + file.filename
    # with open(f'{destination_file_path}', 'wb') as buffer:
    #     shutil.copyfileobj(file.file, buffer)

    new_video = models.Video(name=request.name, description=request.description, videoPath=request.videoPath,
                             uploadDate=datetime.now(), deleteDate=datetime.now(), idUser=user_id)
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video


def destroy(id: int, db: Session):
    video = db.query(models.Video).filter(models.Video.id == id)

    if not video.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Video with id {id} not found")

    video.delete(synchronize_session=False)
    db.commit()
    return 'done'


def update(id: int, request: schemas.Video, db: Session):
    video = db.query(models.Video).filter(models.Video.id == id)

    if not video.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Video with id {id} not found")

    video.update(request)
    db.commit()
    return 'updated'


def show(id: int, db: Session):
    video = db.query(models.Video).filter(models.Video.id == id).first()
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Video with the id {id} is not available")
    return video
