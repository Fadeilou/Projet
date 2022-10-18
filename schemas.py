from typing import Optional, List

from pydantic import BaseModel
from pydantic.schema import date


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserId(BaseModel):
    id: int

    class Config:
        orm_mode = True


class BaseProfile(BaseModel):
    idUser: int
    fullname: str
    pathProfile: str


class Profile(BaseProfile):
    class Config:
        orm_mode = True


class BaseVideo(BaseModel):
    idUser = int
    name: str
    description: str
    videoPath: str


class Video(BaseVideo):
    class Config:
        orm_mode = True


class VideoPath(BaseModel):
    videoPath: str


class AnalysisResult(BaseModel):
    idVideo: int
    startDateOfAnalyse: str
    endDateOfAnalyse: str
    numberOfPeopleDetected: int
    ageProportionDetected: str
    genderProportionDetected: str
    emotionProportionDetected: str
    raceProportionDetected: str
    proportionEmotionAccordingAgeGenderRace: str


class ShowEmotionProportion(BaseModel):
    emotionProportionDetected: str


class ShowRaceProportion(BaseModel):
    raceProportionDetected: str


class ShowGenderProportion(BaseModel):
    genderProportionDetected: str


class ShowAgeProportion(BaseModel):
    ageProportionDetected: str


class ShowProportionAccordingMultiParameter(BaseModel):
    proportionEmotionAccordingAgeGenderRace: str


class BaseHistorical(BaseModel):
    idUser: int
    idAnalysisResult: int


class Historical(BaseHistorical):
    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    username: str
    email: str
    profile: List[Profile] = []
    videos: List[Video] = []
    historicales: List[Historical] = []

    class Config:
        orm_mode = True


class ShowProfile(BaseModel):
    fullname: str
    pathProfile: str
    creator: ShowUser

    class Config:
        orm_mode = True


class ShowVideo(BaseModel):
    name: str
    videoPath: str
    description: str
    uploadDate: str
    uploader: ShowUser
    analysisResultat = AnalysisResult

    class Config:
        orm_mode = True


class ShowAnalysisResult(BaseModel):
    startDateOfAnalyse: str
    endDateOfAnalyse: str
    numberOfPeopleDetected: int
    ageProportionDetected: str
    genderProportionDetected: str
    emotionProportionDetected: str
    raceProportionDetected: str
    proportionEmotionAccordingAgeGenderRace: str
    analyse: ShowVideo

    class Config:
        orm_mode = True


class ShowHistorical(BaseModel):
    userHistorical = ShowUser
    generator: ShowAnalysisResult


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
