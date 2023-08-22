from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel
from db_models.crud import getResponses
from db_models.database import Base, Session, engine
from db_models.models import Questions
from fastapi.encoders import jsonable_encoder
from db_models.models import quesResponse
from db_models.models import calculateScore
from typing import List
Base.metadata.create_all(bind=engine)

session = Session()
app = FastAPI()


@app.get("/hraQuestions/clinical")
async def get_questions(response_model=list[Questions]):
        return (getResponses(session,"Clinical"))

@app.get("/hraQuestions/lifestyle")
async def get_questions(response_model=list[Questions]):
        return (getResponses(session,"Lifestyle"))

@app.get("/hraQuestions/mental")
async def get_questions(response_model=list[Questions]):
        return (getResponses(session,"Mental"))

@app.get("/hraQuestions/nutrition")
async def get_questions(response_model=list[Questions]):
        return (getResponses(session,"Nutrition"))

@app.get("/hraQuestions/fitness")
async def get_questions(response_model=list[Questions]):
        return (getResponses(session,"Fitness"))

@app.post("/hraResponses")
async def get_body(items:list[quesResponse]):
        #print(items)
        a=calculateScore(items)
        return (calculateScore.returnJson(a))
        #return (items)