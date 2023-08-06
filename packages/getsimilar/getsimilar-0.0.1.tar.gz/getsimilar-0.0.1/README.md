# Get similar images
![](https://habrastorage.org/webt/v9/tx/kt/v9txktskofqdmkgamde_wg-1pwk.jpeg)

This tool is a wrapper over an API that returns similar images to a given image.

You can find a demo of the tool [here](https://ternaus.com/).


The description of the API can be found [here](https://ternaus.com/api).

## Installation

```bash
pip install -U getsimilar
```

## Get an API token
* Log in at: [https://ternaus.com/login](https://ternaus.com/login)
* Go to the account page: [https://ternaus.com/account](https://ternaus.com/account)
* Generate new token and save json file with it to `~/.ternaus/ternaus.json`

## Usage
You pass:
* Image in the form of the `numpy` array or `PIL` image.
* URL to the image:
* Text query, for example: "Girls in weird hats"

All requests have a parameter `num_similar` that specifies the number of similar images to return.
This number is capped at 20. If you would like to get more similar images per request, please contact us at [https://www.ternaus.com/#contact](https://www.ternaus.com/#contact).

### From image

```python
from getsimilar import from_image

urls = from_image('path/to/image.jpg', num_similar=<the number of similar images>)
```

### From URL

```python
from getsimilar import from_url

urls = from_url(url, num_similar=<the number of similar images>)
```

### From text

```python
from getsimilar import from_url

urls = from_text(text. num_similar=<the number of similar images>)
```
