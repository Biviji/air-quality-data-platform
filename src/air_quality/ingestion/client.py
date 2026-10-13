import requests

from air_quality.config import OPENAQ_API_KEY, OPENAQ_BASE_URL

class OpenAQClient:

    def __init__(self):
        self.base_url = OPENAQ_BASE_URL
        self.api_key = OPENAQ_API_KEY

    def get(self, endpoint: str, params: dict | None = None) -> dict:

        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        headers = {
            "X-API-Key": self.api_key
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        return response.json()