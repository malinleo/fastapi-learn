from fastapi import FastAPI
from apps.learn.app import router as app_router

app = FastAPI()
app.include_router(app_router)
