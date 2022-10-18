import os
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
import EmotionAnalyse
import schemas


def get_all(db: Session):
    resultats = db.query(models.AnalysisResult).all()
    return resultats


def get_by_video(idVideo: int, db: Session):
    resultats = db.query(models.AnalysisResult).filter(models.AnalysisResult.idVideo == idVideo).first()
    return resultats


def show(id: int, db: Session):
    resultat = db.query(models.AnalysisResult).filter(models.AnalysisResult.id == id).first()
    if not resultat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Resultats with the id {id} is not available")
    return resultat


def create(idVideo: int, db: Session):
    video: schemas.Video = db.query(models.Video).filter(models.Video.id == idVideo).first()
    nb = db.query(models.AnalysisResult).count()
    video_path = video.videoPath
    id_user = video.idUser
    modeles = EmotionAnalyse.EmotionAnalyse.build_model()
    startDateOfAnalyse= datetime.now()
    EmotionAnalyse.EmotionAnalyse.video_analyse(video_path, modeles)
    endDateOfAnalyse = datetime.now()
    numberOfPeopleDetected= EmotionAnalyse.EmotionAnalyse.count_people("public/data.csv")
    ageProportionDetected = EmotionAnalyse.EmotionAnalyse.age_proportion("public/data.csv")
    genderProportionDetected = EmotionAnalyse.EmotionAnalyse.gender_proportion("public/data.csv")
    emotionProportionDetected = EmotionAnalyse.EmotionAnalyse.emotion_proportion("public/data.csv")
    raceProportionDetected = EmotionAnalyse.EmotionAnalyse.race_proportion("public/data.csv")
    proportionEmotionAccordingAgeGenderRace = EmotionAnalyse.EmotionAnalyse.emotion_proportion_according_paramater(
        "public/data.csv")

    new_resultats = models.AnalysisResult(startDateOfAnalyse=startDateOfAnalyse,
                                          endDateOfAnalyse=endDateOfAnalyse,
                                          numberOfPeopleDetected=numberOfPeopleDetected,
                                          ageProportionDetected=ageProportionDetected,
                                          genderProportionDetected=genderProportionDetected,
                                          emotionProportionDetected=emotionProportionDetected,
                                          raceProportionDetected=raceProportionDetected,
                                          proportionEmotionAccordingAgeGenderRace=proportionEmotionAccordingAgeGenderRace,
                                          idVideo=idVideo)
    new_historical = models.Historical(idUser=id_user, idAnalysisResult=nb+1)
    db.add(new_resultats)
    db.add(new_historical)
    db.commit()
    db.refresh(new_resultats)

    if os.path.exists('public/data.csv'):
        os.remove('public/data.csv')

    return new_resultats
