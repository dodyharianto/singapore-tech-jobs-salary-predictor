# Singapore Tech Jobs Salary Predictor

An end-to-end Machine Learning pipeline and REST API that predicts monthly base salaries for Tech roles in Singapore.

<p align="center">
  <img src="docs/assets/app_ui_display_1.png" alt="App UI" width="600" />
  <br />
  <strong>Salary Predictor App Display</strong>
</p>

## 💡 Project Overview
Job seekers often lack transparency in tech salaries in Singapore as most job openings do not disclose salary information. This makes it difficult for candidates to negotiate effectively and for employers to benchmark competitive compensation. This project aims to bridge this gap by building a predictive machine learning model that estimates the lower bound (min) and upper bound (max) of a salary based on the job title, company name, as well as semantic content of a job listing: bullet points of job descriptions, tech stacks, and company details.

## 🛠️ Tech Stack & Architecture
* **Data Ingestion:** Apify (JobStreet Web Scraper), Google SerpAPI
* **Data Versioning:** Data Version Control (DVC)
* **Data Processing & EDA:** Pandas, Matplotlib, Seaborn
* **Machine Learning:** Scikit-Learn, Joblib (Model Packaging)
* **Backend API:** FastAPI, Uvicorn, Pydantic (Data Validation)
* **Frontend UI:** Tailwind CSS

## 🔁 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/dodyharianto/singapore-tech-jobs-salary-predictor.git
cd singapore-tech-jobs-salary-predictor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI server
```bash
cd app
uvicorn app.main:app --reload
```

### 4. Test the prediction endpoint
Navigate to http://127.0.0.1:8000/docs in your browser to use the Swagger UI and test the `/predict` endpoint with a JSON payload consisting of job details.
