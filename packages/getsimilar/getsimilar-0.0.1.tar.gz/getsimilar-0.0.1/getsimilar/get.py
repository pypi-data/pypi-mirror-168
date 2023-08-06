import json

import requests
from image2base64.converters import rgb2base64

from getsimilar.config import API_URL
from getsimilar.utils import (
    ImageType,
    get_ternaus_token,
    get_urls_from_response,
    resize,
)

TARGET_SIZE = 400

headers = {
    "content-type": "application/json",
    "x-api-key": get_ternaus_token(),
}


def get(body: dict) -> dict:
    result = requests.post(API_URL, data=json.dumps(body), headers=headers)

    if result.status_code == 200:
        return result.json()
    if result.status_code == 401:
        raise ValueError("Missing API key")
    if result.status_code == 403:
        raise ValueError("Invalid API key, visit Ternaus.com/account to get a new one.")

    raise ValueError("Invalid request")


def from_url(url: str, num_similar: int = 1) -> list[str]:
    body = {"url": url, "num_similar": num_similar}
    return get_urls_from_response(get(body))


def from_image(image: ImageType, num_similar: int = 1) -> list[str]:
    image = resize(image, TARGET_SIZE)
    body = {"image": rgb2base64(image), "num_similar": num_similar}
    return get_urls_from_response(get(body))


def from_text(text: str, num_similar: int = 1) -> list[str]:
    body = {"text": text, "num_similar": num_similar}
    return get_urls_from_response(get(body))
