from dotenv import load_dotenv
from functools import lru_cache
import os
import pathlib
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from .airtable import Airtable
BASE_DIR = pathlib.Path(__file__).parent  # src


app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")
# http://localhost:3000/abc # route -> # path


@lru_cache()
def cached_dotenv():
    load_dotenv()


cached_dotenv()
# print("AIRTABLE_BASE_ID", os.environ.get("AIRTABLE_BASE_ID"))

AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = os.environ.get("AIRTABLE_TABLE_NAME")


@app.get("/")
async def say_hi():
    return {"message": "Hello World"}


@app.get("/wallet_address/{wallet_address}")
async def check_whitelist(request: Request, wallet_address):
    """
    TODO add CSRF for security
    """
    # to send email to airtable
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
        table_name=AIRTABLE_TABLE_NAME,
    )

    did_retrieve = airtable_client.retrieve_record(wallet_address)

    return {"message": did_retrieve}
