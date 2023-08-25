from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects import postgresql
from .database import Base
from pydantic import BaseModel
import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from typing import List, Optional
class Questions(Base):
   __tablename__ = 'hraquestions'
   
   question_id = Column(Integer, primary_key = True)
   question = Column(String)

   question_responses = Column(postgresql.ARRAY(String))
   answer_type = Column(Integer)
   question_category=Column(String)

   def to_json(self):
      return{
         "question_id":self.question_id,
         "question":self.question,
         "question_responses":self.question_responses,
         "answer_type":self.answer_type
      }

class quesResponse(BaseModel):
   id: str
   response: str

class responseList(BaseModel):
   age: int
   gender:str
   answers: list[quesResponse]
class params(BaseModel):
    n_neighbors:int=5
    return_distance:bool=False

class PredictionIn(BaseModel):
    calorie_goal:float
    ingredients:list[str]=[]
    params:Optional[params]

class Recipe(BaseModel):
    Name:str
    CookTime:str
    PrepTime:str
    TotalTime:str
    RecipeIngredientParts:list[str]
    Calories:float
    FatContent:float
    SaturatedFatContent:float
    CholesterolContent:float
    SodiumContent:float
    CarbohydrateContent:float
    FiberContent:float
    SugarContent:float
    ProteinContent:float
    RecipeInstructions:list[str]

class PredictionOut(BaseModel):
    output: Optional[list[Recipe]] = None
class calculateScore():
   lifestyleScore = 0
   clinicalScore = 0
   fitnessScore = 0 
   mentalScore = 0
   nutritionScore = 0
   completeHealthScore = 0
   clinicalRecommendations = []
   lifestyleRecommendations = []
   wellnessRecommendations = []
   age = 0
   gender = "male"
   ht = 0
   wt = 0
   bmi = 0.0
   bmr = 0
   exerciseFactor = 1.2
   bmiCategory = "Normal"
   def __init__(self,responses):
      #for res in responses:
         #print (res)
      self.lifestyleScore = 0
      self.clinicalScore = 0
      self.fitnessScore = 0
      self.mentalScore = 0
      self.nutritionScore = 0
      self.completeHealthScore = 0
      self.clinicalRecommendations = []
      self.lifestyleRecommendations = []
      self.wellnessRecommendations = []
      #self.age = responses.age
      #self.gender = responses.gender
      bmiFlag = False
      for res in responses.answers:
         if res.id == "height":
            self.ht = int(res.response) 
            #self.ht = self.ht * 2.54
         elif res.id == "weight":
            self.wt = int(res.response)
            
         if res.id == "age":
            self.age == int(responses.age)
         if res.id == "gender":
            self.gender = int(responses.gender)

         if self.ht != 0 and self.wt != 0 and bmiFlag == False:
            self.bmi = self.wt / ((self.ht * 0.01)**2)
            if self.bmi < 18.5:
               self.lifestyleScore+=10
               self.bmiCategory = "Underweight"
            elif self.bmi >=18.5 and self.bmi <24.99:
               self.lifestyleScore+=40
               self.bmiCategory = "Normal"
            elif self.bmi >25 and self.bmi < 29.99:
               self.lifestyleScore+=20
               self.bmiCategory = "Overweight"
            elif self.bmi > 30:
               self.bmiCategory = "Obese"
            bmiFlag = True

         if res.id == "ongoingMedicalCondition" or res.id == "ongoingSymptoms":
            if res.response.lower() == "no":
               self.clinicalScore+=40
            
         if res.id == "alcohol":
            if res.response.lower() == "no":
               self.lifestyleScore+=40
            else:
               self.lifestyleRecommendations.append("Restrict Alcohol consumption 1-2 drink/week")
         if res.id == "tobacco":
            if res.response.lower() == "no":
               self.lifestyleScore+=40
            else:
               self.lifestyleRecommendations.append("Restrict smoking  to 1 stick per day")         
         if res.id == "pastDoctorVisit" or res.id == "pastBloodTest":
            if res.response.lower() == "yes":
               self.clinicalScore+=40
            else:
               self.lifestyleRecommendations.append("Vsit your treating doctor every 6 months")
         if res.id == "bloodSugar":
            if res.response == "Less than 5.6":
               self.clinicalScore+=10
               self.clinicalRecommendations.append("Visit your doctor to get HbA1c checked")
            elif res.response == "Between 5.6 and 5.79":
               self.clinicalScore+=40
            elif res.response == "Between 5.8 and 6.49,":
               self.clinicalScore+=20
               self.clinicalRecommendations.append("You are in pre-diabetic range. Cut down on sugar intake.")
            elif res.response == "HbA1c >= 6.5 Or FBS >=125 Or RBS >= 200":
               self.clinicalRecommendations.append("Repeat HbA1c test every 6 months")
            else:
               self.clinicalRecommendations.append("Visit your doctor to get your HbA1c checked")

         if res.id == "bloodPressure":
            if res.response == ">140/100 mmHg":
               #self.clinicalScore+=10
               self.clinicalRecommendations.append("Visit your doctor and get Blood Pressure Tested")
            elif res.response == "130-139/90 to 99 mmHg":
               self.clinicalScore+=20
               self.clinicalRecommendations.append("Repeat Blood Pressure Test every 6 months")
            elif res.response == "120-80 mmHg or below":
               self.clinicalScore+=40
            self.clinicalRecommendations.append("Visit your doctor to get your Blood Pressure checked")

         if res.id == "cholestrol":
            if res.response == "More than 240":
               #self.clinicalScore+=10
               self.clinicalRecommendations.append("Repeat cholestrol Test every 6 months")
            elif res.response == "Between 200 to 240":
               self.clinicalScore+=20
               self.lifestyleRecommendations.append("Reduce deep fried food to reduce cholestrol")
            elif res.response == "Less than 200":
               self.clinicalScore+=40
            else:
               self.clinicalRecommendations.append("Visit your doctor to get your cholestrol checked")

         if res.id == "medicalConditioninFamily" or res.id == "surgicalHistory":
            if res.response.lower() == "no":
               self.clinicalScore+=40
            
         if res.id == "sleep":
            if res.response == "Less than 6 hrs":
               self.lifestyleScore+=10
               self.lifestyleRecommendations.append("Try to get a minimum sleep of 8 hours per day.")
            elif res.response == "6 to 8 hrs":
               self.lifestyleScore+=20
               self.lifestyleRecommendations.append("Try to get a minimum sleep of 8 hours per day.")
            elif res.response == "More than 8 hours":
               self.lifestyleScore+=40
            

         if res.id == "workLifeBalance":
            if res.response == "Yes":
               self.mentalScore+=20
            elif res.response == "Often":
               self.mentalScore+=10
               self.wellnessRecommendations.append("Adapt time of 20 mins for your hobby or walk with music")
            elif res.response == "Rarely":
               self.mentalScore+=10
               self.wellnessRecommendations.append("Adapt time of 20 mins for your hobby or walk with music")
            else:
               self.wellnessRecommendations.append("Adapt time of 20 mins for your hobby or walk with music")

         if res.id == "stressed":
            if res.response == "Daily":
               self.mentalScore+=0
               self.wellnessRecommendations.append("Identify reasons of stress, pen down thoughts before sleep")
            elif res.response == "Often":
               self.mentalScore+=10
               self.wellnessRecommendations.append("Take time of 30 mins for any physical activity ")
            elif res.response == "Rarely":
               self.mentalScore+=10
               self.wellnessRecommendations.append("Take time of 30 mins for any physical activity")
            else:
               self.mentalScore+=20
         
         if res.id == "exercise":
            if res.response == "5-6 time a week":
               self.fitnessScore+=40
               
            elif res.response == "2-3 times a week":
               self.fitnessScore+=20
               self.lifestyleRecommendations.append("Try to get some exercise for around 4-5 days/week")
               
            elif res.response == "once a week":
               self.fitnessScore+=10
               self.lifestyleRecommendations.append("Initiate 20 mins of day for any physical activity")
               
            else:
               self.lifestyleRecommendations.append("Initiate 20 mins of day for any physical activity")
               

         if res.id == "workProfile":
            if res.response == "Sitting more than 8hrs":
               self.lifestyleScore+=0
            elif res.response == "Long Standing hours":
               self.lifestyleScore+=10
            elif res.response == "Travelling":
               self.lifestyleScore+=10
            elif res.response == "Field work/Household work":
               self.lifestyleScore+=20

         if res.id == "waterConsumption":
            if res.response == "1-2 glass per day":
               self.nutritionScore+=0
               self.wellnessRecommendations.append("Drink a minimum of 4 -5  glass/day")
            elif res.response == "Less than 6 glasses per day":
               self.nutritionScore+=10
               self.wellnessRecommendations.append("Increase water intake to 8 glass/day")
            elif res.response == "6-8 glasses per day":
               self.nutritionScore+=10
               self.wellnessRecommendations.append("Increase water intake to 8 glass/day")
            elif res.response == "More than 8 glass per day":
               self.nutritionScore+=20

         if res.id == "junkFood":
            if res.response == "Daily":
               self.nutritionScore+=0
               self.lifestyleRecommendations.append("Restrict consumption to 1-2 times/week ")
            elif res.response == "Weekly":
               self.nutritionScore+=10
               self.lifestyleRecommendations.append("Indulgence once in a while is healthy behavior")
            elif res.response == "Ocassionally":
               self.nutritionScore+=10
               self.lifestyleRecommendations.append("Reducing Ingulgence in Junk food is beneficial")
            elif res.response == "Rarely":
               self.nutritionScore+=20
         
         if res.id == "fruitsVegetables":
            if res.response == "Absolutely":
               self.nutritionScore+=40
            elif res.response == "Often":
               self.nutritionScore+=30
            elif res.response == "Rarely":
               self.nutritionScore+=10
         #adding steps
         if res.id == "steps":
            if res.response == "Below 5000":
               self.exerciseFactor = 1.2
               self.fitnessScore+=10
            elif res.response == "5000-7500":
               self.fitnessScore+=20
               self.exerciseFactor = 1.375
            elif res.response == "7501-10000":
               self.fitnessScore+=30
               self.exerciseFactor = 1.55
            elif res.response =="Above 10000":
               self.fitnessScore+=40
               self.exerciseFactor = 1.7
      
      if self.clinicalScore != 0:
         self.clinicalScore = (self.clinicalScore / 360) * 100
      if self.fitnessScore != 0:
         self.fitnessScore = (self.fitnessScore / 80) * 100
      if self.lifestyleScore !=0:
         self.lifestyleScore = (self.lifestyleScore / 220) * 100
      if self.mentalScore!=0:
         self.mentalScore = (self.mentalScore / 40) * 100
      if self.nutritionScore != 0:
         self.nutritionScore = (self.nutritionScore / 80) * 100
      
      self.completeHealthScore = (0.3 * self.clinicalScore) + (0.3 * self.lifestyleScore) + (0.1 * self.nutritionScore) + (0.15 * self.fitnessScore) + (0.15 * self.mentalScore)
      if self.gender == "male":
         self.bmr = ((13.397 * self.wt) + (4.79 * self.ht) - (5.67 * self.age) + 88.362) * self.exerciseFactor
      else:
         self.bmr = ((9.24 * self.wt) + (3.09 * self.ht) - (4.33 * self.age) +447.593 ) * self.exerciseFactor
   def returnJson(a):
      return{
         "category":a.bmiCategory,
         "lifestyleScore":a.lifestyleScore,
         "clinicalScore":a.clinicalScore,
         "mentalScore":a.mentalScore,
         "fitnessScore":a.fitnessScore,
         "nutritionScore":a.nutritionScore,
         "completeHealthScore":a.completeHealthScore,
         "clinicalRecommendations":a.clinicalRecommendations,
         "lifestyleRecommendations":a.lifestyleRecommendations,
         "wellnessRecommendations":a.wellnessRecommendations,
         "caloriesToMaintainWeight": a.bmr,
         "-0.25kgPerWeek": (a.bmr*0.9),
         "-0.5kgPerWeek": (a.bmr*0.8),
         "-1kgPerWeek":(a.bmr*0.6),
         "healthScoreInfo":{
            "key":"value",
         }
      }

def scaling(dataframe):
    scaler=StandardScaler()
    prep_data=scaler.fit_transform(dataframe.iloc[:,6:15].to_numpy())
    return prep_data,scaler

def nn_predictor(prep_data):
    neigh = NearestNeighbors(metric='cosine',algorithm='brute')
    neigh.fit(prep_data)
    return neigh

def build_pipeline(neigh,scaler,params):
    transformer = FunctionTransformer(neigh.kneighbors,kw_args=params)
    pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])
    return pipeline

def extract_data(dataframe,ingredients):
    extracted_data=dataframe.copy()
    extracted_data=extract_ingredient_filtered_data(extracted_data,ingredients)
    return extracted_data
    
def extract_ingredient_filtered_data(dataframe,ingredients):
    extracted_data=dataframe.copy()
    regex_string=''.join(map(lambda x:f'(?=.*{x})',ingredients))
    extracted_data=extracted_data[extracted_data['RecipeIngredientParts'].str.contains(regex_string,regex=True,flags=re.IGNORECASE)]
    return extracted_data

def apply_pipeline(pipeline,_input,extracted_data):
    _input=np.array(_input).reshape(1,-1)
    return extracted_data.iloc[pipeline.transform(_input)[0]]

def recommend(dataframe,_input,ingredients=[],params={'n_neighbors':5,'return_distance':False}):
        extracted_data=extract_data(dataframe,ingredients)
        if extracted_data.shape[0]>=params['n_neighbors']:
            prep_data,scaler=scaling(extracted_data)
            neigh=nn_predictor(prep_data)
            pipeline=build_pipeline(neigh,scaler,params)
            return apply_pipeline(pipeline,_input,extracted_data)
        else:
            return None
   
def extract_quoted_strings(s):
    # Find all the strings inside double quotes
    strings = re.findall(r'"([^"]*)"', s)
    # Join the strings with 'and'
    return strings

def output_recommended_recipes(dataframe):
    if dataframe is not None:
        output=dataframe.copy()
        output=output.to_dict("records")
        for recipe in output:
            recipe['RecipeIngredientParts']=extract_quoted_strings(recipe['RecipeIngredientParts'])
            recipe['RecipeInstructions']=extract_quoted_strings(recipe['RecipeInstructions'])
    else:
        output=None
    return output