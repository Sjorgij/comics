import requests
import os


def request_vk_api(method, params):
    url = f"https://api.vk.com/method/{method}"
    response = requests.get(url, params=params)
    return response.json()


def upload_picture(url, picture):
    with open(picture, 'rb') as file:
        files = {
            "photo": file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()


def save_uploaded_picture(params, picture):
    params.update(picture)
    return request_vk_api("photos.saveWallPhoto", params.copy())


def post_picture(picture, post_message, params):
    params_extension = {
        "owner_id": f"-{params['group_id']}",
        "message": post_message,
        "attachments": [f"photo{picture['owner_id']}_{picture['id']}"],
        "from_group": 1,
    }
    params.update(params_extension)
    params.pop("group_id")

    return request_vk_api("wall.post", params.copy())


def create_vk_post(picture_description, picture_path, group_id, access_token):
    params = {
        "access_token": access_token,
        "group_id": group_id,
        "v": 5.131
    }
    upload_url = request_vk_api("photos.getWallUploadServer", params.copy())["response"]["upload_url"]
    uploaded_picture = upload_picture(upload_url, picture_path)
    saved_picture = save_uploaded_picture(params.copy(), uploaded_picture)["response"][0]
    request_log = post_picture(saved_picture, picture_description, params.copy())
    if "error" in request_log.keys():
        print(f"Ошибка! Код ошибки: {request_log['error']['error_code']}, сообщение от сервиса: {request_log['error']['error_msg']}")
