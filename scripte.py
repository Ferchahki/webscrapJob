import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

def export(results):
    df = pd.DataFrame(results)
    df.to_csv("job_results.csv",mode="a", index=False, header=True)
def scrape_jobs():
    job_search = "python"
    base_url = "https://uk.indeed.com/"
    url = base_url + f"jobs?q={job_search}&l=&from=search0nHP"
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    bs = BeautifulSoup(response.text, "html.parser")
    job_list = bs.find('ul', {'class': 'jobsearch-ResultsList'})
    # print(job_list)
    info=[]
    if job_list:
        jobs = job_list.findAll('div', {'class': 'job_seen_beacon'})
        for job in jobs:
            TITLE = job.find('h2', {'class': 'jobTitle'})
            title = TITLE.text
            link = TITLE.find('a').attrs['data-jk']
            url = f'https://uk.indeed.com/viewjob?jk={link}&tk=1h232lii9j9jh801&from=serp&vjs='
            company_name = job.find('span', {"class": "companyName"}).text
            company_location = job.find("div", {"class": "companyLocation"}).text
            print(link,title,url,company_location)
            data = {
                'title': title,
                'company name': company_name,
                 'company location': company_location,
                 'url': url
            }
            info.append(data)
        export(info)
    else:
        print("Job list not found.")

if __name__ == "__main__":
    scrape_jobs()