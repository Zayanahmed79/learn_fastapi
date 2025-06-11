# put & delete api 
from fastapi import FastAPI , Query , HTTPException , Path
from pydantic import BaseModel , Field, computed_field
from typing import Annotated , Optional ,Literal
from fastapi.responses import JSONResponse
import json


app = FastAPI()


def load_data():
    with open('patients.json' , 'r') as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("patients.json", "w") as f:
         json.dump(data, f)



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




class Patient_update(BaseModel):
    name : Annotated[ Optional[str],  Field( default=None,  description="Name of the Patient")]
    city : Annotated[Optional[str] , Field(default=None, description="City where patient lives")]
    age : Annotated[Optional[int], Field( gt=0 , lt = 120, default=None, description="How old Patient is now")]
    gender : Annotated[Optional[Literal['Male', 'Female', 'others']], Field(default=None , description="Gender of Patient")]
    height : Annotated[Optional[float], Field(gt = 0, default=None,  description="Height of the Patient")] 
    weight : Annotated[Optional[float], Field( gt = 0, default=None, description="Weight of Patient")]



@app.put('/put/{patient_id}')
def update_patient(patient_id : str , patient_update : Patient_update):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="Patient not found")


    existing_patient_info = data[patient_id]

    updated_patient_info =  patient_update.model_dump(exclude_unset=True)

    for key , value in updated_patient_info.items():
        existing_patient_info[key] = value

    # existing_patient_info -> into pydantic Patient obj for --> updated bmi and verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj =  Patient(**existing_patient_info)

    # pydantic Patient obj -> agai into dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id') # type: ignore

    # add this dict to data
    data[patient_id] = existing_patient_info

    #save data
    save_data(data)

    return HTTPException(status_code=200 , detail="Patient Updated")



@app.delete('/delete/{patient_id}')
def delete_patient(patient_id : str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="Patient not found")

    del data[patient_id]

    save_data(data)

    return HTTPException(status_code=200 , detail= "Patient deleted successfully!")


    

