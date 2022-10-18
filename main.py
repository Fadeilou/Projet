from fastapi import FastAPI, UploadFile, File
import models
from database import engine
from routers import profiles, users, authentication, videos, historicales, video_analyses
import shutil

app = FastAPI()

app.post("/upload_model")


models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(videos.router)
app.include_router(video_analyses.router)
app.include_router(historicales.router)


