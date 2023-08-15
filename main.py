from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel
from db_models.crud import getResponses
from db_models.database import Base, Session, engine
from db_models.models import Questions
from fastapi.encoders import jsonable_encoder

Base.metadata.create_all(bind=engine)

session = Session()
app = FastAPI()


@app.get("/hraQuestions/Clinical")
async def get_questions(response_model=list[Questions]):
        return (getResponses(session,"Clinical"))

@app.get("/hraQuestions/Lifestyle")
async def get_questions(response_model=list[Questions]):
        return (getResponses(session,"Lifestyle"))

@app.get("/hraQuestions/Mental")
async def get_questions(response_model=list[Questions]):
        return (getResponses(session,"Mental"))

@app.get("/hraQuestions/Nutrition")
async def get_questions(response_model=list[Questions]):
        return (getResponses(session,"Nutrition"))

@app.get("/hraQuestions/Fitness")
async def get_questions(response_model=list[Questions]):
        return (getResponses(session,"Fitness"))