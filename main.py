import requests
from pprint import pprint
import json
from yandex import Yandex
from vk import VK
from backuper import Backuper
from google1 import GoogleDrive

vk_access_token = 'vk1.a.Pc4ZGpU_lSDH5eZGKfNNWVKZQD_8Bo4M_M6BzK-0JmIC_RECWtb70NRGPAFzQQT7H6vHdYQNKY12C' \
                  'BzhQQfDRmicx_XJYPyORjdFmTJJbEF0RkGN-WGChoOV0ZAdCkoxG2cfBLDhITQowNgc7QQH9UqCvyiD1qAQTOF' \
                  '9E-9L40ILqjS9i_TluMYH8LXukO8X'
yandex_token = ""
user_id = '699113813'

vk = VK(vk_access_token, user_id)
# ya = Yandex(yandex_token)
path_to_backup = '/netology/vk_backup/'


def backup_fotos_from_album(path_to_save, album_id='profile', foto_count=5, disk_to_save='Yandex'):
    backuper = Backuper(yandex_token, disk=disk_to_save)
    folder_id = backuper.get_new_folder_path(path_to_save)
    if isinstance(backuper, GoogleDrive):
        path_to_save = folder_id

    fotos = vk.get_photos_from_albom(album_id=album_id)
    # pprint(fotos)
    json_data = []
    for foto in fotos['response']['items']:
        if foto_count >= 0:
            foto_likes = str(foto['likes']['count'])
            foto_id = str(foto['id'])
            sizes = 's, m, x, o, p, q, r, y, z, w'
            picture_url = sorted(foto['sizes'], key=lambda x: sizes.find(x['type']))
            picture = requests.get(picture_url[-1]['url']).content
            picture_name = f'{foto_id}_{foto_likes}_likes.jpg'
            backuper.upload_data_to_disk(path_to_save, picture_name, picture)
            json_data.append({'file_name': picture_name, 'size': 'w'})
            foto_count -= 1
    json_file_name = f'fotos_info_album_{album_id}.json'
    with open(json_file_name, 'w') as f:
        json.dump(json_data, f)
    backuper.upload_file_to_disk(path_to_save, json_file_name)


def backup_all_albums(path_to_save, *args, **kwargs):
    # ya.get_new_folder_path(path_to_save)
    albums = vk.get_albums()
    # pprint(albums)
    for album in albums["response"]['items']:
        folder_name = album['title']
        album_id = album['id']
        path = path_to_save + folder_name + '/'
        backup_fotos_from_album(path, album_id=album_id, *args, **kwargs)


if __name__ == '__main__':
    # backup_fotos_from_album(path_to_backup, disk_to_save='Yandex')  # Yandex или Google
    backup_all_albums(path_to_backup, disk_to_save='Google')  # Yandex или Google
