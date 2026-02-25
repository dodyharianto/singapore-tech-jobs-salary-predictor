from fastapi import FastAPI
import pandas as pd
import joblib
from app.job_features import JobFeatures

app = FastAPI(title="SG Tech Jobs Salary Predictor API", version="1.0")

model = joblib.load('./models/xgb_baseline_v1.pkl')

@app.get("/")
def health_check():
    return {"message": "ok"}

@app.post("/predict")
def predict_salary(job: JobFeatures):
    input_data = pd.DataFrame([{
        'location': job.location,
        'classifications/0/sub': job.classification_sub,
        'workTypes/0': job.work_type,
        'python': job.python,
        'llm': job.llm,
        'data': job.data,
        'production': job.production,
        'ai': job.ai,
        'sql': job.sql,
        'cloud': job.cloud,
        'senior': job.senior,
        'java': job.java,
        'javascript': job.javascript,
        'security': job.security
    }])

    prediction = model.predict(input_data)
    return {"predicted_salary": float(prediction[0])}