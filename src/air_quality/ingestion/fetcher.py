
from air_quality.ingestion.client import OpenAQClient


class OpenAQFetcher:
    def __init__(self, client: OpenAQClient):
        self.client = client

    def fetch_all(
        self,
        endpoint: str,
        params: dict | None = None,
        page_size: int = 100,
        max_pages: int = 10,
    ) -> list[dict]:

        if page_size <= 0 or max_pages <= 0:
            raise ValueError("page_size and max_pages must be positive")

        all_records = []
        base_params = dict(params or {})

        for page in range(1, max_pages + 1):
            request_params = {
                **base_params,
                "limit": page_size,
                "page": page,
            }

            data = self.client.get(
                endpoint,
                params=request_params
            )

            records = data["results"]
            all_records.extend(records)

            print(f"Page {page}: {len(records)} records")

            if len(records) < page_size:
                break

        return all_records
