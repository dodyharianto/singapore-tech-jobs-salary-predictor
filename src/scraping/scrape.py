from apify_client import ApifyClient
import os
import pandas as pd
import serpapi
from dotenv import load_dotenv
from datetime import datetime
import logging

load_dotenv()
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
API_KEY = os.getenv('APIFY_API_KEY')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_jobstreet(max_items=50_000):
    try:
        client = ApifyClient(API_KEY)
        URLS = ['https://sg.jobstreet.com/jobs-in-information-communication-technology/in-Singapore']
        run_input = {
            "jobSearchUrls": URLS,
            "maxItems": max_items,
            "scrapeJobDescription": True,
            "proxyConfiguration": { "useApifyProxy": False },
        }

        ACTOR_ID = os.getenv('APIFY_ACTOR_ID')
        run = client.actor(ACTOR_ID).call(run_input=run_input)

        df = pd.DataFrame(list(client.dataset(run["defaultDatasetId"]).iterate_items()))
        df['data_source'] = 'JobStreet'
        logger.info(f'Gathered {len(df)} of JobStreet via Apify.')
        return df
    except Exception as e:
        logger.error('Something went wrong when scraping JobsStreet via Apify.')
        return None

def scrape_google_jobs(query='tech jobs', page_limit=5):
    try:
        client = serpapi.Client(api_key=SERPAPI_API_KEY)
        page_number = 1
        query = 'tech jobs'
        jobs_with_salary = []

        search_params = {
            'engine': 'google_jobs',
            'q': query,
            'location': 'Singapore',
            'google_domain': 'google.com.sg',
            'hl': 'en',
            'gl': 'sg',
        }

        while page_number <= page_limit:
            try:
                results = client.search(search_params)
                jobs = results['jobs_results']
                logger.info(f'\nFound {len(jobs)} jobs on page {page_number + 1}.')

                if len(jobs) == 0:
                    logger.info('No more jobs found.')
                    break

                for job in jobs:
                    detected_extensions = job.get('detected_extensions', {})
                    if 'salary' in detected_extensions.keys():
                        jobs_with_salary.append({
                            'title': job['title'],
                            'company_name': job['company_name'],
                            'job_title': job['job_title'],
                            'description': job['description'],
                            'salary': detected_extensions['salary'],
                        })

                if 'serpapi_pagination' in results and 'next_page_token' in results['serpapi_pagination']:
                    next_page_token = results['serpapi_pagination']['next_page_token']
                    search_params['next_page_token'] = next_page_token
                    page_number += 1
                else:
                    break
            except Exception as e:
                logger.error(f'Error scraping page: {page_number}: {e}')
                break

        jobs_with_salary_df = pd.DataFrame(jobs_with_salary)
        jobs_with_salary_df['data_source'] = 'Google Jobs'
        jobs_with_salary_df['scraped_at'] = datetime.now().isoformat()

        logger.info(f'Scraped {len(jobs_with_salary_df)} jobs from Google Jobs with salary.')
        return jobs_with_salary_df
    except Exception as e:
        logger.error(f"Error scraping Google Jobs: {e}")
        return None

def save_raw_data(df, source):
    if df is None or len(df) == 0:
        logger.warning(f"No data to save for {source}")
        return None
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(script_dir, '../../data/raw')

    try:
        output_dir = os.path.join(base_dir, source.lower())
    except Exception as e:
        logger.error(f'Error finding job source: {source.lower()}')
        raise ValueError(f'Unknown source: {source}')
    
    os.makedirs(output_dir, exist_ok=True)

    filename = f'{source.lower()}_{date_str}.csv'
    output_path = os.path.join(output_dir, filename)
    
    df.to_csv(output_path, index=False)
    logger.info(f'Saved {len(df)} records to {output_path}')
    return output_path