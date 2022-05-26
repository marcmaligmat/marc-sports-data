import time
from msilib.schema import Class
from typing import List


class Scraper:
    def __init__(
        self,
        scraper: Class,
        website: str,
        league: str,
    ):
        print("Starting scraper")
        self.start = time.perf_counter()
        self.scraper = scraper
        self.website = website
        self.league = league

    def __enter__(self):
        return self.scraper.scrape()

    def __exit__(self, type, value, traceback):
        print("\nClosing Scraper")
        elapsed = time.perf_counter() - self.start

        print(
            f"[{self.league}]: Scraped {self.website} finished in {elapsed} seconds.\n"
        )

    def scrape(self) -> List:
        ...

    def parse(self) -> dict:
        """Assigning of keys in values for result"""

    def handle_results(self, results: list):
        """Handles a batch of results. This function should store the results, possibly in a database."""
        pass
