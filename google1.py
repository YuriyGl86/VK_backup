from __future__ import print_function
from pprint import pprint

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaInMemoryUpload


# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/drive.file']


class GoogleDrive:

    def __init__(self, creds=None, SCOPES='https://www.googleapis.com/auth/drive.file', *args, **kwargs):
        self.creds = creds
        self.SCOPES = [SCOPES]
        self.get_authorization()

    def get_authorization(self):

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def upload_data_to_disk(self, path_to_save, picture_name, picture):
        try:
            # create gmail api client
            service = build('drive', 'v3', credentials=self.creds)
            file_metadata = {
                'title': 'pppppp',
                'name': picture_name,
                'parents': [path_to_save],
            }

            media = MediaInMemoryUpload(picture, mimetype='image/jpeg', resumable=True)
            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(F'File {picture_name} has added to the folder with ' F'ID "{path_to_save}".')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file.get('id')

    def upload_file_to_disk(self, path_to_save, file_name):
        try:
            # create gmail api client
            service = build('drive', 'v3', credentials=self.creds)
            file_metadata = {
                'title': 'pppppp',
                'name': file_name,
                'parents': [path_to_save],

            }

            media = MediaFileUpload(file_name, mimetype='image/jpeg', resumable=True)
            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(F'File {file_name} has added to the folder with ' F'ID "{path_to_save}".')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file.get('id')

    def get_new_folder(self, name, parent='root'):
        try:
            # create gmail api client
            service = build('drive', 'v3', credentials=self.creds)
            file_metadata = {
                'title': 'Invoices',
                'name': name,
                'parents': [parent],
                'mimeType': 'application/vnd.google-apps.folder'
            }

            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, fields='id').execute()
            print(F'Folder {name} has created with ID: "{file.get("id")}".')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file.get('id')

    def get_new_folder_path(self, folder_path):
        foldres = folder_path.strip('/').split('/')
        folder_id = self.get_new_folder(foldres[0])
        for subfolder in foldres[1:]:
            folder_id = self.get_new_folder(subfolder, parent=folder_id)

        return folder_id

    def get_file_list(self):
        try:
            service = build('drive', 'v3', credentials=self.creds)

            results = service.files().list(fields="nextPageToken, files(id, name, mimeType, parents)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            print('Files:')
            for item in items:
                print(item)
                print(item['parents'])
            return items
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')


    def check_path_for_existing(self, folder_name, parent='root'):
        file_list = self.get_file_list()
        if file_list:
            for file in self.get_file_list():

                if file['name'] == folder_name and file['mimeType'] == 'application/vnd.google-apps.folder' and \
                        file['parents'] == parent:
                    return file['id']
        return
