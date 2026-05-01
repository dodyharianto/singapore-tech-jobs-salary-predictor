from fastapi import FastAPI
import pandas as pd
import joblib
from job_features import JobFeatures
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI(title='SG Tech Jobs Salary Predictor API', version='1.0')

class JobTextRequest(BaseModel):
    description: str

def parse_job_description(description: str) -> dict:
    description = description.lower()
    input_data = {
        'text_corpus': description,
    }
    return input_data

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(os.path.dirname(current_dir), "static")
models_dir = os.path.join(os.path.dirname(current_dir), "models")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

model_pkl_filename = 'rf_tf_idf_corpus_only.pkl'
model_path = os.path.join(models_dir, model_pkl_filename)
model = joblib.load(model_path)

@app.get("/")
def display_ui():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/health")
def health_check():
    return {"message": "ok"}

@app.post("/predict")
def predict_salary(request: JobTextRequest):
    raw_job_description = request.description
    features = parse_job_description(raw_job_description)

    input_data = pd.DataFrame([features])
    prediction = model.predict(input_data)
    return {"predicted_salary": int(prediction[0])}