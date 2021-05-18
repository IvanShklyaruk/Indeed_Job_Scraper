import csv
from os import write
import requests
from bs4 import BeautifulSoup

# Generates a url depending on job position and a canadian city
def generate_url(pos, city):
    template = 'https://ca.indeed.com/jobs?q={}&l={}'
    url = template.format(pos, city)
    return url

# Obtains a job's data
def obtain_job_data(job):
    atag = job.h2.a
    j_title = atag.get('title')
    j_url = 'https://ca.indeed.com' + atag.get('href')
    company = job.find('span', 'company').text.strip()
    j_location = job.find('div', 'recJobLoc').get('data-rc-loc')
    j_summary = job.find('div', 'summary').text.strip()
    post_date = job.find('span', 'date').text
    try:
        j_salary = job.find('span', 'salaryText').text.strip()
    except AttributeError:
        j_salary = ''

    record = (j_title, company, j_location, post_date,j_summary, j_salary, j_url)

    return record


def search_jobs(pos, city):
    records = []
    url = generate_url(pos, city)

    # extract the job data
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('div', 'jobsearch-SerpJobCard')

        for job in jobs:
            record = obtain_job_data(job)
            records.append(record)
        try:
            url = 'https://ca.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break

    # save the job data
    with open('results.csv','w', newline = '', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Job Title', 'Company Name', 'Location', 'Post Date', 'Summary', 'Salary', 'Job Link'])
        writer.writerows(records)

# Example: search_jobs('software developer', 'toronto')

search_jobs('software developer', 'toronto')




    
    