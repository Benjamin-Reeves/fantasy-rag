from pydantic import BaseModel
import requests


class WebScrape(BaseModel):
    url: str
    headers: dict = {}

    def fetch_content(self) -> str:
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching content from {self.url}: {e}")
            return ""