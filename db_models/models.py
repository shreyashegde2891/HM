from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects import postgresql
from .database import Base

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