import logging
from os import makedirs, remove
from typing import List
from os.path import join
from zipfile import ZipFile

from yadisk import YaDisk
from yadisk.exceptions import PathNotFoundError

logger = logging.getLogger(__name__)

N_RETRIES = 999


class YaSimpleFile:
    def __init__(self, client: 'YaSimpleClient', name: str, root: str, ya_full_path: str):
        """
        Файл для загрузки на локальную машину
        :param client: YandexClient для загрузки
        :param name: Название файла
        :param root: Полный путь до папки загрузки
        :param ya_full_path: Полный путь до ресурса в YandexClient
        """
        self._name = name
        self._root = root
        self._client = client
        self._ya_full_path = ya_full_path

    def save(self) -> str:
        """
        Сохраняет выбранный файл в директорию
        :return: Возвращает полный путь до файла
        """
        self._client.save_files([self])
        return self.fullpath

    @property
    def fullpath(self) -> str:
        """
        Выводит полный путь до файла.
        Перед этим не забудьте сохранить файл
        """
        return join(self._root, self._name)

    @property
    def name(self) -> str:
        """
        Выводит имя файла с расширением
        """
        return self._name

    def __repr__(self):
        return repr(f"<{self.__class__.__name__} filename='{self.name}' path='{self.fullpath}'>")


class YaSimpleClient:
    def __init__(self, root_folder_save: str = None):
        self.client = YaDisk()
        self.root_folder_save = root_folder_save or 'resource'
        self.url = 'https://disk.yandex.ru/d/qNVky6OJfWRrjw'
        self.DETECT = '/detect'
        self.ALL = '/all'

    def path_folder(self, *dest) -> str:
        dest = map(lambda item: item.strip("/"), dest)
        return join(self.root_folder_save, *dest)

    def barcode(self, barcode: str) -> List[YaSimpleFile]:
        """
        Получить список файлов документов по строке баркода
        :param barcode: 13-ти символьная строка
        :return: Список из файлов, если существует комплект документов.
        Если не существует, вернет пустой список
        """
        try:
            logger.info(f"Запрашивется комплект документов {barcode}")
            ya_full_path = f"{self.DETECT}/{barcode}"
            root = self.path_folder(self.DETECT, barcode)
            resources = self.client.public_listdir(
                public_key=self.url, n_retries=N_RETRIES, path=ya_full_path,
                fields=['type', 'name']
            )
            result = []
            for resource in resources:
                if resource.type == 'file':
                    result.append(
                        YaSimpleFile(
                            client=self,
                            name=resource.name,
                            root=root,
                            ya_full_path=f"{ya_full_path}/{resource.name}"
                        )
                    )
            return result

        except PathNotFoundError:
            return []

    def all_barcodes(self) -> List[str]:
        """
        Получить список доступных отсканированных баркодов
        """
        try:
            logger.info(f"Запрашивется все доступные баркоды")
            resources = self.client.public_listdir(
                public_key=self.url, n_retries=N_RETRIES, path=self.DETECT,
                fields=['type', 'name']
            )
            result = []
            for resource in resources:
                if resource.type == 'dir':
                    result.append(
                        resource.name
                    )
            return result
        except PathNotFoundError:
            return []

    def save_files(self, files: List[YaSimpleFile]):
        """
        Сохраняет файлы
        :param files: Список файлов для сохранения полученные ресурсами
        """
        for file in files:
            makedirs(file._root, exist_ok=True)
            self.client.download_public(
                public_key=self.url,
                path=file._ya_full_path,
                file_or_path=file.fullpath,
                n_retries=N_RETRIES,
            )

    def synchronize_all(self) -> List[str]:
        """
        Синхронизирует все доступные документы из папки ALL
        :return: Возвращает список путей до файлов
        """
        result = []
        path_file_resource = self.path_folder('all.zip')
        self.client.download_public(
            public_key=self.url,
            path=self.ALL,
            file_or_path=path_file_resource,
            n_retries=N_RETRIES
        )
        with ZipFile(path_file_resource) as file:
            for filename in file.namelist():
                file.extract(filename, self.root_folder_save)
                if filename and filename[-1] != '/':
                    result.append(self.path_folder(filename))
        remove(path_file_resource)
        return result


Client = YaSimpleClient()

__all__ = (
    "YaSimpleClient",
    "YaSimpleFile",
    "Client",
)
