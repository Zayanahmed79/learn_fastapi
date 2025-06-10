from fastapi import FastAPI ,  Path , HTTPException ,Query
import json


app = FastAPI()

def load_data():
    with open("patients.json","r") as f:
        data = json.load(f)
    return data


@app.get("/view")
def view():
    data = load_data()

    return data
    


@app.get("/")
def hello():
    return {'message':'Hello World!'}

@app.get("/about")
def about():
    return {
            "message": "Zayan is a millionaire!"
    }



@app.get("/patient/{patient_id}")
def view_patients(patient_id : str  = Path(..., description="ID of patients in DB.", example="P001")):
    data = load_data() 

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404 , detail= 'Patient not found!')





@app.get("/sort")
def sort_patients(sort_by : str = Query(..., description=f"Sort on the basis of height, weight or bmi "), order: str = Query('asc', description="sort in asc and desc order")):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid fields select from {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid field select from asc and desc")
    
    data = load_data()

    sort_data = True if order == "desc" else False 

    sorted_data = sorted(data.values(), key=lambda x : x.get(sort_by, 0), reverse=sort_data)

    return sorted_data


