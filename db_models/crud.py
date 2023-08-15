from . import models
from sqlalchemy.orm import Session
from sqlalchemy.ext.serializer import loads, dumps
def getResponses(db:Session,question_category: str):
    print("Crud Called")
    print("Issuing Command")
    result = db.query(models.Questions).filter(models.Questions.question_category.match("%Clinical%"))
    serialized = [z.to_json() for z in result]
    print(serialized)
    return (serialized)
    #print (result)
    #result_list = []
    #for row in result:
        #json_row=json.loads({"question_id:", row.question_id, "question: ",row.question, "question_responses:",row.question_responses, "answer_type:",row.answer_type, "question_category:",row.question_category})
        #result_list.append(["question_id:", row.question_id, "question: ",row.question, "question_responses:",row.question_responses, "answer_type:",row.answer_type, "question_category:",row.question_category])
        #result_list.append(json_row)
    
    #json_string = json.dumps(result_list)
    #print(result_list)
    #return(result_list)