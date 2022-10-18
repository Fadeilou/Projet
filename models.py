from datetime import date

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    profile = relationship("Profile", back_populates="creator")
    videos = relationship("Video", back_populates="uploader")
    historicales = relationship("Historical", back_populates="userHistorical")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    idUser = Column(Integer, ForeignKey("users.id"))
    fullname = Column(String, index=True)
    pathProfile = Column(String, index=True, nullable=True)

    creator = relationship("User", back_populates="profile")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    idUser = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    videoPath = Column(String, index=True)
    description = Column(String, index=True)
    uploadDate = Column(String, index=True)
    deleteDate = Column(String, index=True, nullable=True)

    uploader = relationship("User", back_populates="videos")
    analysisResultat = relationship("AnalysisResult", back_populates="analyse")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    idVideo = Column(Integer, ForeignKey("videos.id"))
    startDateOfAnalyse = Column(String, index=True)
    endDateOfAnalyse = Column(String, index=True)
    numberOfPeopleDetected = Column(String, index=True)
    ageProportionDetected = Column(String, index=True)
    genderProportionDetected = Column(String, index=True)
    emotionProportionDetected = Column(String, index=True)
    raceProportionDetected = Column(String, index=True)
    proportionEmotionAccordingAgeGenderRace = Column(String, index=True)

    analyse = relationship("Video", back_populates="analysisResultat")
    historicales = relationship("Historical", back_populates="generator")


class Historical(Base):
    __tablename__ = "historicals"

    id = Column(Integer, primary_key=True, index=True)
    idUser = Column(Integer, ForeignKey("users.id"))
    idAnalysisResult = Column(Integer, ForeignKey("analysis_results.id"))

    userHistorical = relationship("User", back_populates="historicales")
    generator = relationship("AnalysisResult", back_populates="historicales")