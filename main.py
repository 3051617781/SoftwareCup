import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import config
from database import Base, engine
from service.user import user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists("./avatar/"):
    os.makedirs("./avatar/")

app.mount("/avatar", StaticFiles(directory="avatar"), name="avatar")
app.mount("/upload", StaticFiles(directory="upload"), name="upload")
app.include_router(user_router, prefix="/user")



@app.get("/")
async def root():
    return {
        "status": 0,
        "message": "OK",
        "version": "v1.0.0"
    }


if __name__ == "__main__":
    uvicorn.run(app, host=config.bind_host, port=config.bind_port)
