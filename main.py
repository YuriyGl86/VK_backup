import requests
from pprint import pprint

from yandex import Yandex
from vk import VK


access_token = 'vk1.a.Pc4ZGpU_lSDH5eZGKfNNWVKZQD_8Bo4M_M6BzK-0JmIC_RECWtb70NRGPAFzQQT7H6vHdYQNKY12C' \
               'BzhQQfDRmicx_XJYPyORjdFmTJJbEF0RkGN-WGChoOV0ZAdCkoxG2cfBLDhITQowNgc7QQH9UqCvyiD1qAQTOF' \
               '9E-9L40ILqjS9i_TluMYH8LXukO8X'

user_id = '699113813'
vk = VK(access_token, user_id)
print(vk.users_info())
qq = vk.get_photos()
print(qq)
# print(vk.get_alboms())
with open('foto.jpg', 'wb') as f:
    foto = requests.get(qq['response']['items'][0]['sizes'][0]['url']).content
    f.write(foto)
