import tarfile
import os


class VirtualFileSystem:
    def __init__(self, tar_path):
        self.tar_path = tar_path

    def list_files(self):
        """Возвращает список файлов внутри архива tar."""
        with tarfile.open(self.tar_path, 'r') as tar:
            return tar.getnames()

    def open_file(self, filename):
        """Открывает файл из архива tar и возвращает его содержимое."""
        with tarfile.open(self.tar_path, 'r') as tar:
            try:
                file = tar.extractfile(filename)
                return file.read().decode('utf-16')
            except KeyError:
                return f"Файл {filename} не найден в архиве"

    # def open_file(self, filename):
    #     """Открывает файл из архива tar и возвращает его содержимое."""
    #     with tarfile.open(self.tar_path, 'r') as tar:
    #         try:
    #             file = tar.extractfile(filename)
    #             if file is None:
    #                 return f"Файл {filename} не найден в архиве"
    #
    #             try:
    #                 # Попытка декодировать содержимое как UTF-8
    #                 return file.read().decode('utf-8')
    #             except UnicodeDecodeError:
    #                 # Если файл не в UTF-8, возвращаем двоичные данные или сообщение об ошибке
    #                 return f"Ошибка: файл {filename} не является текстовым или имеет некорректную кодировку."
    #         except KeyError:
    #             return f"Файл {filename} не найден в архиве"

    def check_file(self, filename):
        """Проверяет наличие файла в архиве tar"""
        with tarfile.open(self.tar_path, 'r') as tar:
            try:
                file = tar.extractfile(filename)
                return True
            except KeyError:
                return False
