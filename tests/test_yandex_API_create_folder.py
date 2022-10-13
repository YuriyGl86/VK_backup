import unittest
from yandex import Yandex

with open('../yandex_token.txt', encoding='utf-8') as file:
    yandex_token = file.read().strip()

ya = Yandex(yandex_token)


class TestYandexAPI(unittest.TestCase):
    test_folder_name = '/тестовая_папка_yandex_API'

    def test_create_folder(self):
        result = ya.get_new_folder(self.test_folder_name)
        self.assertEqual(result, 201)

    def tearDown(self) -> None:
        ya.delete_folder(self.test_folder_name)