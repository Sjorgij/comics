import os

from downlad_random_comix import download_comics
from create_vk_post import create_vk_post


def main():
    comix_description, comics_path = download_comics()
    create_vk_post(comix_description, comics_path)
    os.remove(comics_path)


if __name__ == "__main__":
    main()
