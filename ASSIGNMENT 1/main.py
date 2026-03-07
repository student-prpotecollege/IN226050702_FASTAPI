from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI working successfully"}

@app.get("/student")
def student():
    return {"name": "Saloni", "course": "FastAPI Internship"}

@app.get("/course")
def course():
    return {"course": "FastAPI", "duration": "1 month"}