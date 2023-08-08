import requests


def get_upload_server(access_token, group_id, api_version):
    params = {
        "access_token": access_token,
        "group_id": group_id,
        "v": api_version
    }
    url = f"https://api.vk.com/method/photos.getWallUploadServer"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["response"]["upload_url"]


def upload_picture(url, picture_path):
    with open(picture_path, 'rb') as file:
        files = {
            "photo": file,
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    return response.json().values()


def save_uploaded_picture(access_token, group_id, api_version, upload_server, picture, picture_hash):
    params = {
        "access_token": access_token,
        "group_id": group_id,
        "v": api_version,
        "server": upload_server,
        "photo": picture,
        "hash": picture_hash
    }
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()["response"][0]
    return response["owner_id"], response["id"]


def post_picture(post_owner_id, picture_owner_id, picture_id, access_token, api_version, post_message):
    params = {
        "access_token": access_token,
        "owner_id": f"-{post_owner_id}",
        "message": post_message,
        "attachments": [f"photo{picture_owner_id}_{picture_id}"],
        "from_group": 1,
        "v": api_version
    }
    url = "https://api.vk.com/method/wall.post"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def create_vk_post(picture_description, picture_path, group_id, access_token):
    api_version = 5.131
    upload_url = get_upload_server(access_token, group_id, api_version)
    upload_server, picture, picture_hash = upload_picture(upload_url, picture_path)
    picture_owner_id, picture_id = save_uploaded_picture(access_token, group_id, api_version, upload_server, picture, picture_hash)
    request_log = post_picture(group_id, picture_owner_id, picture_id, access_token, api_version, picture_description)
    if "error" in request_log.keys():
        print(f"Ошибка! Код ошибки: {request_log['error']['error_code']}, сообщение от сервиса: {request_log['error']['error_msg']}")
