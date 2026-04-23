from apify_client import ApifyClient
import os
import pandas as pd
import serpapi
from dotenv import load_dotenv

load_dotenv()
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
API_KEY = os.getenv('APIFY_API_KEY')
DATA_PATH = '../../data/sg-tech-jobs.csv'

def scrape_jobstreet():
    client = ApifyClient(API_KEY)
    URLS = ['https://sg.jobstreet.com/jobs-in-information-communication-technology/in-Singapore']
    run_input = {
        "jobSearchUrls": URLS,
        "maxItems": 50_000,
        "scrapeJobDescription": True,
        "proxyConfiguration": { "useApifyProxy": False },
    }

    ACTOR_ID = os.getenv('APIFY_ACTOR_ID')
    run = client.actor(ACTOR_ID).call(run_input=run_input)

    df = pd.DataFrame(list(client.dataset(run["defaultDatasetId"]).iterate_items()))
    df['data_source'] = 'JobStreet'
    return df

def scrape_google_jobs(query, page_number_limit):
    client = serpapi.Client(api_key=SERPAPI_API_KEY)
    page_number = 0
    jobs_with_salary = []
    while page_number <= page_number_limit:
        search_params = {
            'engine': 'google_jobs',
            'q': query,
            'location': 'Singapore',
            'google_domain': 'google.com.sg',
            'hl': 'en',
            'gl': 'sg',
        }

        results = client.search(search_params)
        jobs = results['jobs_results']
        print(f'\nFound {len(jobs)} jobs on page {page_number + 1}.')
        print(jobs)
        if len(jobs) == 0:
            print('No more jobs found.')
            break

        for job in jobs:
            detected_extensions = job.get('detected_extensions', {})
            print('\nDetected extensions for this job')
            print(detected_extensions)
            if 'salary' in detected_extensions.keys():
                jobs_with_salary.append({
                    'title': job['title'],
                    'company_name': job['company_name'],
                    'job_title': job['job_title'],
                    'description': job['description'],
                    'salary': detected_extensions['salary'],
                })

        next_page_token = results['serpapi_pagination']['next_page_token']
        if next_page_token:
            search_params['next_page_token'] = next_page_token
        else:
            break
        page_number += 1

    jobs_with_salary_df = pd.DataFrame(jobs_with_salary)
    jobs_with_salary_df['data_source'] = 'Google Jobs'
    return jobs_with_salary_df