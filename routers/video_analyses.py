from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import database
import oauth2
import schemas
from repository import video_analyses

router = APIRouter(
    prefix="/video_analyse",
    tags=['video_analyses']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowAnalysisResult])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return video_analyses.get_all(db)


@router.get('/{id}', response_model=schemas.ShowAnalysisResult)
def get_by_video(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return video_analyses.get_by_video(id, db)


@router.post('/{id_video}', status_code=status.HTTP_201_CREATED, )
def create(id_video: int, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    return video_analyses.create(id_video, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return video_analyses.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.AnalysisResult, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    return video_analyses.update(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowAnalysisResult)
def show(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return video_analyses.show(id, db)


@router.get('/show_emotion_proportion/{id}', status_code=200, response_model=schemas.ShowEmotionProportion)
def show_emotion_proportion(id: int, db: Session = Depends(get_db),
                            current_user: schemas.User = Depends(oauth2.get_current_user)):
    return video_analyses.show(id, db)


@router.get('/show_gender_proportion/{id}', status_code=200, response_model=schemas.ShowGenderProportion)
def show_gender_proportion(id: int, db: Session = Depends(get_db),
                           current_user: schemas.User = Depends(oauth2.get_current_user)):
    return video_analyses.show(id, db)


@router.get('/show_race_proportion/{id}', status_code=200, response_model=schemas.ShowRaceProportion)
def show_race_proportion(id: int, db: Session = Depends(get_db),
                         current_user: schemas.User = Depends(oauth2.get_current_user)):
    return video_analyses.show(id, db)


@router.get('/show_age_proportion/{id}', status_code=200, response_model=schemas.ShowAgeProportion)
def show_age_proportion(id: int, db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(oauth2.get_current_user)):
    return video_analyses.show(id, db)


@router.get('/show_proportion_according_multi_parameter/{id}', status_code=200, response_model=schemas.ShowProportionAccordingMultiParameter)
def show_proportion_according_multi_parameter(id: int, db: Session = Depends(get_db),
                                              current_user: schemas.User = Depends(oauth2.get_current_user)):
    return video_analyses.show(id, db)
