from fastapi import FastAPI
import pandas as pd
import joblib
from job_features import JobFeatures
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title='SG Tech Jobs Salary Predictor API', version='1.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobTextRequest(BaseModel):
    job_title: str
    company_name: str
    job_description: str

def parse_input(job_title: str, company_name: str, job_description: str) -> dict:
    text_corpus = f'{job_title.lower()} {company_name.lower()} {job_description.lower()}'
    input_data = {
        'text_corpus': text_corpus,
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
    job_title = request.job_title
    company_name = request.company_name
    job_description = request.job_description
    
    if not job_title:
        return {"error": "Please input job title."}
    if not company_name:
        company_name = 'Tech Company'
    if len(job_description.split()) < 30:
        return {"error": "Please provide more details of the job description for better predictions."}
    
    features = parse_input(job_title, company_name, job_description)
    input_data = pd.DataFrame([features])
    prediction = model.predict(input_data)
    return {"predicted_salary": int(prediction[0])}