# app/modules/scraper.py

import requests
from bs4 import BeautifulSoup # type: ignore

def scrape_company_info(company_name):
    try:
        search_url = f"https://en.wikipedia.org/wiki/{company_name.replace(' ', '_')}"
        response = requests.get(search_url)

        if response.status_code != 200:
            return f"Could not retrieve information for {company_name}."

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")

        info = ""
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 40:
                info += text + "\n"
            if len(info) > 1000:
                break

        return info if info else f"No suitable info found on Wikipedia for {company_name}."
    except Exception as e:
        return f"Error while scraping data: {str(e)}"
