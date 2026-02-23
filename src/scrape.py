from apify_client import ApifyClient
import os
import pandas as pd

API_KEY = os.getenv('APIFY_API_KEY')
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
df.to_csv('./data/sg-tech-jobs.csv', index=False)