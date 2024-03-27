from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel
from db_models.crud import getResponses
from db_models.database import Base, Session, engine
from db_models.models import Questions
from fastapi.encoders import jsonable_encoder
from db_models.models import quesResponse
from db_models.models import responseList
from db_models.models import calculateScore
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from db_models.models import recommend,output_recommended_recipes
from db_models.models import params, PredictionIn, Recipe, PredictionOut
from random import uniform as rnd
from fastapi.responses import JSONResponse
from google.cloud import pubsub_v1


project_id = "pruinhlth-nprd-dev-scxlyx-7250"
topic_id = "healthmgt-test"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

Base.metadata.create_all(bind=engine)
dataset=pd.read_csv('data/dataset.csv',compression='gzip')

session = Session()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
#async def get_body(items:list[quesResponse]):
async def get_body(items:responseList):
        res_data_str = f"{jsonable_encoder(items)}"
        res_data = res_data_str.encode("utf-8")
        future = publisher.publish(topic_path, res_data)
        print(future.result())
        a=calculateScore(items)
        return (calculateScore.returnJson(a))
        #return (items)

@app.post("/recommend/breakfast")
def update_item(prediction_input:PredictionIn):
    recommended_nutrition = [prediction_input.calorie_goal * 0.3,rnd(10,30),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,10),rnd(0,10),rnd(30,100)]
    recommendation_dataframe=recommend(dataset,recommended_nutrition,prediction_input.ingredients,prediction_input.params.dict())
    output=output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output":None}
    else:
        return {"output":output}
@app.post("/recommend/lunch")
def update_item(prediction_input:PredictionIn):
    recommended_nutrition = [prediction_input.calorie_goal * 0.5,rnd(10,30),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,10),rnd(0,10),rnd(30,100)]
    recommendation_dataframe=recommend(dataset,recommended_nutrition,prediction_input.ingredients,prediction_input.params.dict())
    output=output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output":None}
    else:
        return {"output":output}
@app.post("/recommend/dinner")
def update_item(prediction_input:PredictionIn):
    recommended_nutrition = [prediction_input.calorie_goal * 0.2,rnd(10,30),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,10),rnd(0,10),rnd(30,100)]
    recommendation_dataframe=recommend(dataset,recommended_nutrition,prediction_input.ingredients,prediction_input.params.dict())
    output=output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output":None}
    else:
        return {"output":output}