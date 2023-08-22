from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects import postgresql
from .database import Base
from pydantic import BaseModel

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
   id: int
   response: str

class responseList(BaseModel):
   age: int
   gender:str
   answers: list[quesResponse]

class calculateScore():
   lifestyleScore = 0
   clinicalScore = 0
   fitnessScore = 0 
   mentalScore = 0
   nutritionScore = 0
   completeHealthScore = 0
   recommendations = []
   age = 0
   gender = "male"
   ht = 0
   wt = 0
   bmi = 0.0
   bmr = 0
   exerciseFactor = 1.2

   def __init__(self,responses):
      #for res in responses:
         #print (res)
      self.lifestyleScore = 0
      self.clinicalScore = 0
      self.fitnessScore = 0
      self.mentalScore = 0
      self.nutritionScore = 0
      self.completeHealthScore = 0
      self.recommendations = []
      self.age = responses.age
      self.gender = responses.gender

      for res in responses.answers:
         if res.id == 1:
            self.ht = int(res.response) 
         elif res.id == 2:
            self.wt = int(res.response)
            self.bmi = self.ht / ((self.wt * 0.01)**2)

            if self.bmi < 18.5:
               self.lifestyleScore+=10
               self.recommendations.append("Underweight: Intiiate 5-7k steps weekly thrice")
            elif self.bmi >=18.5 and self.bmi <24.99:
               self.lifestyleScore+=40
               self.recommendations.append("Normal: Initiate 7k-10k steps weekly 5 times")
            elif self.bmi >25 and self.bmi < 29.99:
               self.lifestyleScore+=20
               self.recommendations.append("Overweight: Complete 7k-10k steps daily")
            elif self.bmi > 30:
               self.recommendations.append("Obese: Complete 7k-10k steps daily")

         if res.id == 3 or res.id == 4:
            if res.response.lower() == "no":
               self.clinicalScore+=40
            
         if res.id ==5:
            if res.response.lower() == "no":
               self.lifestyleScore+=40
            else:
               self.recommendations.append("Restrict Alcohol consumption 1-2 drink/week")
         if res.id == 6:
            if res.response.lower() == "no":
               self.lifestyleScore+=40
            else:
               self.recommendations.append("Restrict smoking  to 1 stick per day")         
         if res.id == 7 or res.id == 8:
            if res.response.lower() == "yes":
               self.clinicalScore+=40
            else:
               self.recommendations.append("Vsit your treating doctor every 6 months")
         if res.id==9:
            if res.response == "HbA1c <5.6 or FBS <60 or RBS <80":
               self.clinicalScore+=10
               self.recommendations.append("Visit your doctor and get HbA1c checked")
            elif res.response == "HbA1c in the range of>= 5.6 to 5.79 OR FBS in the range of > 60 to 100 Or RBS in the range of >=80 to 100":
               self.clinicalScore+=40
            elif res.response == "HbA1c in the range of >= 5.8 to 6.49 Or FBS in the range of>= 101 to 125 Or RBS in the range of >=101 to 140":
               self.clinicalScore+=20
               self.recommendations.append("Repeat HbA1c test every 6 months")
            elif res.response == "HbA1c >= 6.5 Or FBS >=125 Or RBS >= 200":
               self.recommendations.append("Repeat HbA1c test every 6 months")
            else:
               self.recommendations.append("Visit your doctor to get your HbA1c checked")

         if res.id ==10:
            if res.response == ">140/100 mmHg":
               #self.clinicalScore+=10
               self.recommendations.append("Visit your doctor and get Blood Pressure Tested")
            elif res.response == "130-139/90 to 99 mmHg":
               self.clinicalScore+=20
               self.recommendations.append("Repeat Blood Pressure Test every 6 months")
            elif res.response == "120-80 mmHg or below":
               self.clinicalScore+=40
            self.recommendations.append("Visit your doctor to get your Blood Pressure checked")

         if res.id == 11:
            if res.response == "More than 240":
               #self.clinicalScore+=10
               self.recommendations.append("Visit your doctor and get cholestrol Tested")
            elif res.response == "Between 200 to 240":
               self.clinicalScore+=20
               self.recommendations.append("Repeat cholestrol Test every 6 months")
            elif res.response == "Less than 200":
               self.clinicalScore+=40
            else:
               self.recommendations.append("Visit your doctor to get your cholestrol checked")

         if res.id == 12 or res.id == 13:
            if res.response.lower() == "no":
               self.clinicalScore+=40
            
         if res.id == 14:
            if res.response == "Less than 6 hrs":
               self.lifestyleScore+=10
            elif res.response == "6.1-7.9 hrs":
               self.lifestyleScore+=20
            elif res.response == "Around 8 hrs and more":
               self.lifestyleScore+=40
            self.recommendations.append("Adequate amount of Sleep is around 8hrs/day")

         if res.id ==15:
            if res.response == "Daily":
               self.mentalScore+=20
            elif res.response == "Sometimes/ Often":
               self.mentalScore+=10
               self.recommendations.append("Adapt time of 20 mins for your hobby or walk with music")
            elif res.response == "Rarely":
               self.mentalScore+=10
               self.recommendations.append("Adapt time of 20 mins for your hobby or walk with music")
            else:
               self.recommendations.append("Adapt time of 20 mins for your hobby or walk with music")

         if res.id == 16:
            if res.response == "Daily":
               self.mentalScore+=0
               self.recommendations.append("Identify reasons of stress, pen down thoughts before sleep")
            elif res.response == "Sometimes/ Often":
               self.mentalScore+=10
               self.recommendations.append("Take time of 30 mins for any physical activity ")
            elif res.response == "Rarely":
               self.mentalScore+=10
               self.recommendations.append("Take time of 30 mins for any physical activity")
            else:
               self.mentalScore+=20
         
         if res.id == 17:
            if res.response == "Daily 5-6 time/week":
               self.fitnessScore+=40
               self.exerciseFactor = 1.9
            elif res.response == "2-3 times /weekly":
               self.fitnessScore+=20
               self.recommendations.append("Try be more regular for around 4-5 days/week")
               self.exerciseFactor = 1.6
            elif res.response == "once a week":
               self.fitnessScore+=10
               self.recommendations.append("Initiate 20 mins of day for any physical activity")
               self.exerciseFactor = 1.4
            else:
               self.recommendations.append("Initiate 20 mins of day for any physical activity")
               self.exerciseFactor = 1.2
         if res.id == 18:
            if res.response == "Sitting more than 8hrs":
               self.lifestyleScore+=0
            elif res.response == "Long Standing hours":
               self.lifestyleScore+=10
            elif res.response == "Travelling":
               self.lifestyleScore+=10
            elif res.response == "Field work/ Hosuehold work":
               self.lifestyleScore+=20

         if res.id == 19:
            if res.response == "1-2 glass":
               self.nutritionScore+=0
               self.recommendations.append("Drink a minimum of 4 -5  glass/day")
            elif res.response == "Less than 6 glass":
               self.nutritionScore+=10
               self.recommendations.append("Increase water intake to 8 glass/day")
            elif res.response == "6-8 glass":
               self.nutritionScore+=10
               self.recommendations.append("Increase water intake to 8 glass/day")
            elif res.response == "More than 8 glass":
               self.nutritionScore+=20

         if res.id == 20:
            if res.response == "Daily":
               self.nutritionScore+=0
               self.recommendations.append("Restrict consumption to 1-2 times/week ")
            elif res.response == "Weekly":
               self.nutritionScore+=10
               self.recommendations.append("Indulgence once in a while is healthy behavior")
            elif res.response == "Ocassionally":
               self.nutritionScore+=10
               self.recommendations.append("Reducing Ingulgence in Junk food is beneficial")
            elif res.response == "Hardly ever/ rarely":
               self.nutritionScore+=20
      
      if self.clinicalScore != 0:
         self.clinicalScore = (self.clinicalScore / 360) * 100
      if self.fitnessScore != 0:
         self.fitnessScore = (self.fitnessScore / 40) * 100
      if self.lifestyleScore !=0:
         self.lifestyleScore = (self.lifestyleScore / 220) * 100
      if self.mentalScore!=0:
         self.mentalScore = (self.mentalScore / 40) * 100
      if self.nutritionScore != 0:
         self.nutritionScore = (self.nutritionScore / 40) * 100
      
      self.completeHealthScore = (0.3 * self.clinicalScore) + (0.3 * self.lifestyleScore) + (0.1 * self.nutritionScore) + (0.15 * self.fitnessScore) + (0.15 * self.mentalScore)
      if self.gender == "male":
         self.bmr = ((10 * self.wt) + (6.25 * self.ht) - (5 * self.age) + 5) * self.exerciseFactor
      else:
         self.bmr = ((10 * self.wt) + (6.25 * self.ht) - (5 * self.age) -161 ) * self.exerciseFactor
   def returnJson(a):
      return{
         "lifestyleScore":a.lifestyleScore,
         "clinicalScore":a.clinicalScore,
         "mentalScore":a.mentalScore,
         "fitnessScore":a.fitnessScore,
         "nutritionScore":a.nutritionScore,
         "completeHealthScore":a.completeHealthScore,
         "recommendations":a.recommendations,
         "BMR calculation Method":"Mifflin-St Jeor Equation",
         "caloriesToMaintainWeight": str(a.bmr) + "Calories",
         "caloriesToLoseWeight": str(a.bmr-500) + "Calories",
         "caloriesToGainWeight": str(a.bmr+500) + "Calories"
      }
