import os
import json
import httpx
import asyncio
import azure_blob_storage
from datetime import datetime
from dotenv import load_dotenv

# Loading .env
load_dotenv()
random_data_url = os.getenv("RANDOM_DATA_URL")
random_data_key = os.getenv("RANDOM_DATA_KEY")
random_data_peer_batch = 10
random_data_request_limt = 1
random_data_request_sleep_time = 2

azure_blob_container = "randomdata"
azure_blob_folder = "employee"

client = httpx.AsyncClient()
semaphore = asyncio.Semaphore(
    random_data_request_limt
)  # limiting to one request peer time because i don't have another plan, if you can do more requests, increase this number


async def get_random_data(
    client: httpx.AsyncClient, url: str, key: str, sleep: int = None
) -> dict:
    """
    Function that generates random data using the https://random-data-api.com/
    Args:
        client (httpx.AsyncClient): the current httpx async client
        url (str): the random-data url contaiing the project id
        key (str): the random-data key for the project
    """
    async with semaphore:
        response = await client.get(url, headers={"X-API-Key": key})
        if sleep:
            await asyncio.sleep(
                sleep
            )  # sleeping to not get blocked, you can remove if you don't have this kind of problem
        status_code = response.status_code
        print(f"random data - status code {status_code}")
        if status_code == 200:
            return response.json()


async def main() -> None:
    tasks = [
        get_random_data(
            client, random_data_url, random_data_key, random_data_request_sleep_time
        )
        for i in range(random_data_peer_batch)
    ]
    random_data = await asyncio.gather(*tasks)
    load_ts = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    await azure_blob_storage.write_blob(
        container=azure_blob_container,
        filename=f"{azure_blob_folder}/{load_ts}.json",
        content=json.dumps(random_data),
    )
    await client.aclose()


asyncio.run(main())
