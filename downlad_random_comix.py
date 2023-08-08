import requests
from pathlib import Path
from random import randint


def fetch_random_comic_number():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    newest_comics_num = response.json()["num"]
    random_comix_num = randint(1, newest_comics_num)
    return random_comix_num


def download_comic(comix_num=fetch_random_comic_number()):
    url = f"https://xkcd.com/{comix_num}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comics = response.json()
    comics_name = comics["title"]
    comics_description = comics["alt"]
    comics_save_path = Path.cwd() / "comics" / f"{comics_name}.png"
    picture = requests.get(comics["img"])
    picture.raise_for_status()
    with open(comics_save_path, "wb") as image:
        image.write(picture.content)
    return comics_description, comics_save_path
