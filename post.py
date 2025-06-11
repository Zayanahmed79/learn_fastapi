# post api

from fastapi import FastAPI , Path, HTTPException, Query
from pydantic import BaseModel , Field , computed_field
from fastapi.responses import JSONResponse
from typing import Annotated  , Literal
import json


def load_data():
    with open("patients.json" , "r") as f:
        data = json.load(f)
        return data



def save_data(data):
    with open("patients.json", "w") as f:
         json.dump(data, f)

    








app = FastAPI()

class Patient(BaseModel):

    id : Annotated[str, Field(..., description="ID of the Patient", examples=["P001"])]
    name : Annotated[str , Field(..., description="Name of the Patient")]
    city : Annotated[str , Field(..., description="City where patient lives")]
    age : Annotated[int, Field(..., gt=0 , lt = 120, description="How old Patient is now")]
    gender : Annotated[Literal['Male', 'Female', 'others'], Field(..., description="Gender of Patient")]
    height : Annotated[float, Field(..., description="Height of the Patient")] 
    weight : Annotated[float, Field(..., gt = 0, description="Weight of Patient")]



    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi


    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
        

@app.post('/create')
def create_patient(patient : Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400 , detail="Patinet already exists")

    data[patient.id] = patient.model_dump(exclude=['id']) # type: ignore
 
 
    save_data(data)

    return JSONResponse(status_code=201, content={'message' : 'patient created successfully!'})
     
    

@app.get("/")
def hello():
    return {'message':'Hello World!'}






         










