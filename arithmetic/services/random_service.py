import httpx

from arithmetic.settings import settings


async def generate_random_string() -> str:
    """Generates a random string by querying the random.org API."""
    url = "https://api.random.org/json-rpc/4/invoke"
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "method": "generateStrings",
        "params": {
            "apiKey": settings.random,
            "n": 1,
            "length": 32,
            "characters": "abcdefghijklmnopqrstuvwxyz",
            "replacement": True,
        },
        "id": 42,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response_data = response.json()

    # Error handling
    if response.status_code != 200 or "error" in response_data:
        raise Exception(
            f"Error fetching string: {response_data.get('error', 'Unknown error')}",
        )

    return response_data["result"]["random"]["data"][0]
