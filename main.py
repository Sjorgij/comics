import os
from dotenv import load_dotenv

from downlad_random_comix import download_comic
from create_vk_post import create_vk_post


def main():
    load_dotenv()
    group_id = os.environ["GROUP_ID"]
    access_token = os.environ["VK_TOKEN"]
    comix_description, comics_path = download_comic()
    try:
        request_log = create_vk_post(comix_description, comics_path, group_id, access_token)
    finally:
        os.remove(comics_path)
    if "error" in request_log.keys():
        return f"Ошибка! Код ошибки: {request_log['error']['error_code']}, сообщение от сервиса: {request_log['error']['error_msg']}"


if __name__ == "__main__":
    main()
