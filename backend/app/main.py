# backend/app/main.py
from fastapi import FastAPI
from app.routers import auth_router 

app = FastAPI()

app.include_router(auth_router.router)

@app.get("/")
def root():
    return {"message": "Skill Marketplace API is running successfully!"}
