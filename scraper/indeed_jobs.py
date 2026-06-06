"""
Indeed job scraper stub.
Replace the placeholder logic below with real parsing once
you've inspected the site's HTML structure.
"""
from datetime import date
from scraper.common import fetch_page, save_raw
from loguru import logger

SEARCH_URL = "https://www.indeed.com/jobs?q=NISM+finance&location=India"


def scrape(save: bool = True) -> list[dict]:
    """
    Scrape Indeed for NISM-related jobs.
    Returns a list of raw job dicts.
    """
    logger.info("[IndeedScraper] Starting scrape...")
    jobs = []

    # TODO: replace with real parsing logic
    # soup = fetch_page(SEARCH_URL)
    # if not soup:
    #     return []
    # for card in soup.select(".job-card"):
    #     jobs.append({
    #         "company_name": card.select_one(".company").text,
    #         "position":     card.select_one(".title").text,
    #         "location":     card.select_one(".location").text,
    #         "apply_link":   card.select_one("a")["href"],
    #         "source":       "Indeed",
    #         "posted_date":  str(date.today()),
    #     })

    logger.info(f"[IndeedScraper] Found {len(jobs)} jobs")
    if save and jobs:
        save_raw(jobs, "indeed_" + str(date.today()) + ".json")
    return jobs


if __name__ == "__main__":
    results = scrape()
    print(f"Scraped {len(results)} jobs from Indeed")
