from yandex import Yandex
from google1 import GoogleDrive


class Backuper:

    def __new__(cls, *args, **kwargs):
        if kwargs['disk'].lower() == 'yandex':
            obj = super().__new__(Yandex)
        elif kwargs['disk'].lower() == 'google':
            obj = super().__new__(GoogleDrive)
        else:
            raise AttributeError('Неверно указан диск')
        obj.__init__(*args, **kwargs)

        return obj
