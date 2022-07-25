import requests


class Yandex:

    def __init__(self, token):
        self.__token = token

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.__token}'}

    def get_new_folder(self, folder_path):
        link = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': folder_path}
        response = requests.put(link, headers=headers, params=params)
        if response.status_code == 201:
            print("Success")
        else:
            print(response.text)

    def get_new_folder_path(self, folder_path):
        path = '/'
        for subfolder in folder_path.strip('/').split('/'):
            path = path + subfolder.strip('/') + '/'
            self.get_new_folder(path)

    def get_link_for_upload(self, path, overwrite=True):
        link = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': path, 'overwrite': overwrite}
        response = requests.get(link, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, path, file):
        upload_link = self.get_link_for_upload(path)['href']
        with open(file, 'rb') as data:
            response = requests.put(upload_link, data=data)
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

    def upload_data_to_disk(self, path, data):
        upload_link = self.get_link_for_upload(path)['href']
        response = requests.put(upload_link, data=data)
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")
