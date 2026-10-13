import os

from dotenv import load_dotenv


load_dotenv()


OPENAQ_BASE_URL = os.getenv(
    "OPENAQ_BASE_URL",
    "https://api.openaq.org/v3"
)

OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")

if not OPENAQ_API_KEY:
    raise ValueError(
        "OPENAQ_API_KEY is missing. "
        "Add it to your .env file."
    )