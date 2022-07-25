import requests


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_photos_from_albom(self, album_id='profile'):
        url = 'https://api.vk.com/method/photos.get'
        params = {'user_ids': self.id, 'owner_id': self.id, 'album_id': album_id, 'extended': 1, 'photo_sizes': 1}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_albums(self):
        url = 'https://api.vk.com/method/photos.getAlbums'
        params = {'user_ids': self.id, 'need_system': 1}
        response = requests.get(url, params={**self.params, **params})
        return response.json()
