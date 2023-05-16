import logging

import requests

from app.config import settings

log = logging.getLogger("uvicorn")


class WikiApi:
    def __init__(self, domain="wikitech.wikimedia"):
        self.base_url = f"https://{domain}.org/w/api.php"
        self.headers = {"User-Agent": settings.custom_ua}

    def get_wikitext(self, title):
        """Get wikitext for an article."""
        params = {
            "action": "query",
            "prop": "revisions",
            "titles": title.split("#", maxsplit=1)[0],
            "rvslots": "*",
            "rvprop": "content",
            "rvdir": "older",
            "rvlimit": 1,
            "format": "json",
            "formatversion": 2,
        }
        try:
            r = requests.get(url=self.base_url, params=params, headers=self.headers)
            rj = r.json()
            return rj["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
        except Exception as e:
            log.error(f"Failed to get wikitext for title {title}: {e}")
            raise
