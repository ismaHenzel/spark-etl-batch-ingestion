import os
from dotenv import load_dotenv
from azure.storage.blob.aio import BlobServiceClient

load_dotenv()


def create_blob_client():
    return BlobServiceClient(
        account_url=os.getenv("AZURE_BLOB_ACCOUNT_URL"),
        credential={
            "account_name": os.getenv("AZURE_BLOB_ACCOUNT_NAME"),
            "account_key": os.getenv("AZURE_BLOB_ACCOUNT_KEY"),
        },
    )


async def write_blob(
    container: str, filename: str, content: str, overwrite=False
) -> None:
    """
    Function that write files inside azure blob storage
    To Create the client, you need to set the .env variables: AZURE_BLOB_ACCOUNT_NAME, AZURE_BLOB_ACCOUNT_URL, AZURE_BLOB_ACCOUNT_KEY

    Args:
        container (str): storage container name
        filename (str): blob filename (ex: test.json) (you need to specify the type like .json, .csv , etc)
        content_str (str): the content of the blob file

    Example:
        asyncio.run(write_json_blob("randomdata", "test5.json", json.dumps({"teste": "123"})))
    """
    async with create_blob_client() as blob_service_client:
        container_client = blob_service_client.get_container_client(container)
        blob_client = container_client.get_blob_client(filename)
        await blob_client.upload_blob(content, overwrite=overwrite)
