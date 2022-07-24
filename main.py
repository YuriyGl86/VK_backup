import requests
from pprint import pprint

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

   def get_photos(self):
       url = 'https://api.vk.com/method/photos.get'
       params = {'user_ids': self.id, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

   def get_alboms(self):
       url = 'https://api.vk.com/method/photos.getAlbums'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()


access_token = 'vk1.a.Pc4ZGpU_lSDH5eZGKfNNWVKZQD_8Bo4M_M6BzK-0JmIC_RECWtb70NRGPAFzQQT7H6vHdYQNKY12CBzhQQfDRmicx_XJYPyORjdFmTJJbEF0RkGN-WGChoOV0ZAdCkoxG2cfBLDhITQowNgc7QQH9UqCvyiD1qAQTOF9E-9L40ILqjS9i_TluMYH8LXukO8X'

user_id = '699113813'
vk = VK(access_token, user_id)
print(vk.users_info())
pprint(vk.get_photos())
# print(vk.get_alboms())

