import json

import requests
from bs4 import BeautifulSoup


def processJob(job):
    print(f"Job: {job}")
    response = requests.get(job)
    soup = BeautifulSoup(response.text, "html.parser")
    payTxt = "The base pay range for this role is between"
    if payTxt in soup.text:
        pay = soup.text.split(payTxt)[1].split(", and")[0].strip().replace(",", "").replace("annualized", "")
        data = {
            "jobNumber": soup.select_one('strong[id="jobNumber"]').text,
            "title": soup.select_one('h1[id="jdPostingTitle"]').text,
            "department": soup.select_one('div[id="job-team-name"]').text,
            "addressLocality": soup.select_one('span[itemprop="addressLocality"]').text if soup.select_one(
                'span[itemprop="addressLocality"]') else None,
            "addressRegion": soup.select_one('span[itemprop="addressRegion"]').text if soup.select_one(
                'span[itemprop="addressRegion"]') else None,
            "addressCountry": soup.select_one('span[itemprop="addressCountry"]').text if soup.select_one(
                'span[itemprop="addressCountry"]') else None,
            "jobWeeklyHours": soup.select_one('strong[id="jobWeeklyHours"]').text if soup.select_one(
                'strong[id="jobWeeklyHours"]') else None,
            "jobPostDate": soup.select_one('time[datetime]')['datetime'],
            "minPay": int(pay.split("and")[0].strip()[1:]),
            "maxPay": int(pay.split("and")[1].strip()[1:]),
            "payCurrency": pay[0]
        }
    else:
        data = {
            "jobNumber": soup.select_one('strong[id="jobNumber"]').text,
            "title": soup.select_one('h1[id="jdPostingTitle"]').text,
            "department": soup.select_one('div[id="job-team-name"]').text,
            "addressLocality": soup.select_one('span[itemprop="addressLocality"]').text if soup.select_one(
                'span[itemprop="addressLocality"]') else None,
            "addressRegion": soup.select_one('span[itemprop="addressRegion"]').text if soup.select_one(
                'span[itemprop="addressRegion"]') else None,
            "addressCountry": soup.select_one('span[itemprop="addressCountry"]').text if soup.select_one(
                'span[itemprop="addressCountry"]') else None,
            "jobWeeklyHours": soup.select_one('strong[id="jobWeeklyHours"]').text if soup.select_one(
                'strong[id="jobWeeklyHours"]') else None,
            "jobPostDate": soup.select_one('time[datetime]')['datetime'],
            "minPay": None,
            "maxPay": None,
            "payCurrency": None
        }
    print(json.dumps(data, indent=4))


def main():
    url = "https://jobs.apple.com/en-us/search"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pages = int(soup.find_all("span", {"class": "pageNumber"})[-1].get_text())
    print(f"Total number of pages: {pages}")
    for i in range(1, pages + 1):
        print(f"Getting page {i}")
        params = {
            "location": "united-states-USA",
            "page": i
        }
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("a", {"class": "table--advanced-search__title"})
        for job in jobs:
            processJob(f'https://jobs.apple.com{job["href"]}')


if __name__ == '__main__':
    main()
    # processJob("https://jobs.apple.com/en-us/details/114438148/us-business-expert?team=APPST")
