import json
import os
from typing import Union

import numpy as np
from PIL import Image

from getsimilar.config import TOKEN_PATH

ImageType = Union[np.ndarray, Image.Image]


def get_urls_from_response(response):
    return [x["url"] for x in json.loads(response["body"])["images"]]


def get_ternaus_token():
    if "TERNAUS_TOKEN" in os.environ:
        return os.environ["TERNAUS_TOKEN"]
    if TOKEN_PATH.exists():
        return json.loads(TOKEN_PATH.read_text(encoding="utf-8"))["token"]

    raise ValueError("Ternaus token not found. You can get it at https://ternaus.com/account")


def resize(image: ImageType, target_size: int) -> Image.Image:
    if isinstance(image, np.ndarray):
        img = Image.fromarray(image)
    elif isinstance(image, Image.Image):
        img = image
    else:
        raise ValueError(f"image should be np.ndarray or PIL.Image, not {type(image)}")

    if img.size[0] > img.size[1]:
        new_size = (target_size, int(img.size[1] * target_size / img.size[0]))
    else:
        new_size = (int(img.size[0] * target_size / img.size[1]), target_size)

    return img.resize(new_size)
