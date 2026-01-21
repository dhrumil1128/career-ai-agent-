"""
jobs.py
-------
Fetches jobs using JSearch API.
"""

import os
import requests

JSEARCH_KEY = os.getenv("JSEARCH_API_KEY")

def search_jobs(query):
    if not JSEARCH_KEY:
        return ["⚠️ Job search API key not configured"]

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": JSEARCH_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {"query": query, "page": "1", "num_pages": "1"}

    r = requests.get(url, headers=headers, params=params)

    jobs = []
    if r.status_code == 200:
        for job in r.json().get("data", [])[:3]:
            jobs.append(f"{job['job_title']} @ {job['employer_name']}")

    return jobs or ["No jobs found"]
