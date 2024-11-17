import os
import sys
import tarfile
import time
from fs_handler import VirtualFileSystem


class ShellEmulator:
    def __init__(self, username, fs, fs_archive, start_script):
        self.username = username
        self.fs = fs
        self.current_dir = '/'  # Начальная директория в виртуальной файловой системе
        self.virtual_files = {}  # Словарь для хранения "виртуальных" файлов и их содержимого
        self.file_timestamps = {}  # Словарь для хранения "временных меток" виртуальных файлов
        self.fs_path = fs_archive
        self.script_path = start_script

    def prompt(self):
        return f"{self.username}@emulator:{self.current_dir}$ "

    def execute_command(self, command):
        if command == "ls":
            return self.ls()
        elif command.startswith("cd "):
            directory = command.split(" ")[1]
            return self.cd(directory)
        elif command.startswith("touch "):
            filename = command.split(" ")[1]
            return self.touch(filename)
        elif command.startswith("tac "):
            filename = command.split(" ")[1]
            return self.tac(filename)
        elif command == "exit":
            self.exit()
        else:
            return f"Unknown command: {command}"

    def ls(self):
        # Список файлов в текущей директории виртуальной файловой системы, включая виртуальные файлы.
        files = self.fs.list_files()
        current_path = self.current_dir.lstrip('/') + '/' if self.current_dir != '/' else ''
        filtered_files = [f[len(current_path):] for f in files if f.startswith(current_path)]

        # Добавляем виртуальные файлы, созданные командой touch
        virtual_files_in_dir = [
            f[len(current_path):] for f in self.virtual_files.keys() if f.startswith(current_path)
        ]

        return '\n'.join(filtered_files + virtual_files_in_dir)

    def cd(self, directory):
        # Переход в другую директорию (эмуляция).
        if directory == '/':
            self.current_dir = '/'
        elif directory == '..':
            # Переход в родительскую директорию
            if self.current_dir != '/':
                self.current_dir = '/'.join(self.current_dir.rstrip('/').split('/')[:-1]) or '/'
        else:
            # Определяем полный путь (абсолютный или относительный)
            if self.current_dir == '/' and len(self.current_dir) == 1:
                print(self.current_dir)
                possible_path = self.current_dir.rstrip('/') + directory
            elif directory[0] == '/' and len(directory) != 1:
                #  possible_path = self.current_dir.rstrip('/')
                print(self.current_dir)
                print(directory[1:])
                possible_path = directory[1:]
            else:
                print(self.current_dir)
                possible_path = self.current_dir.rstrip('/') + '/' + directory

            # Проверка, существует ли директория в виртуальной файловой системе
            if any(f.startswith(possible_path + '/') or f == possible_path for f in self.fs.list_files()):
                self.current_dir = possible_path
            else:
                return f"Directory not found: {directory}, path - {possible_path}"
        return ""

    # def cd(self, directory):
    # Переход в другую директорию (эмуляция).
    # if directory == '/':
    #     self.current_dir = '/'
    # elif directory == '..':
    # Переход в родительскую директорию
    #     if self.current_dir != '/':
    #         self.current_dir = '/'.join(self.current_dir.rstrip('/').split('/')[:-1]) or '/'
    # else:
    # Проверка, существует ли директория
    # if self.current_dir == '/':
    #     print(self.current_dir)
    #     possible_path = self.current_dir.rstrip('/') + directory
    # else:
    #     print(self.current_dir)
    #     possible_path = self.current_dir.rstrip('/') + '/' + directory
    #  possible_path = self.current_dir.rstrip('/') + directory
    # possible_path = self.current_dir.rstrip(
    #     '/') + '/' + directory if self.current_dir != '/' else '/' + directory
    #  if any(f.startswith(possible_path + '/') for f in self.fs.list_files()):
    #      self.current_dir = possible_path
    #     else:
    #         return f"Directory not found: {directory}, path - {possible_path}"
    # return ""

    def touch(self, filename):
        # Создание пустого файла или обновление времени для существующего.
        current_path = self.current_dir.rstrip('/') + '/' if self.current_dir != '/' else '/'
        file_path = current_path + filename

        # Если файл уже существует в архиве
        if file_path in self.fs.list_files():
            # Извлекаем содержимое архива
            extract_path = "./temp_fs"
            with tarfile.open(self.fs_path, "r") as tar:
                tar.extractall(path=extract_path)

            # Путь к извлеченному файлу
            extracted_file_path = os.path.join(extract_path, file_path.lstrip('/'))
            if os.path.exists(extracted_file_path):
                # Обновляем временную метку
                os.utime(extracted_file_path, None)
                message = f"Метка времени для '{filename}' обновлена."
            else:
                message = f"Ошибка: файл '{filename}' не найден в архиве."

            # Пересоздаем архив с обновленными файлами
            with tarfile.open(self.fs_path, "w") as tar:
                for root, dirs, files in os.walk(extract_path):
                    for file in files:
                        file_full_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_full_path,
                                                  extract_path)  # Относительный путь для правильной структуры
                        tar.add(file_full_path, arcname=arcname)

            # Удаляем временные извлеченные файлы
            for root, dirs, files in os.walk(extract_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

            return message
        # Если файл не существует, создаем пустой  файл и устанавливаем начальную метку времени
        self.virtual_files[file_path] = ""  # Пустое содержимое файла
        self.file_timestamps[file_path] = time.ctime()  # Устанавливаем текущее время как метку времени
     #   return f"Файл '{filename}' создан: {self.file_timestamps[file_path]}"
        return f"Файл '{filename}' создан"
        # Если файл не существует, создаем пустой файл
        # extract_path = "./temp_fs"
        # with tarfile.open(self.fs_path, "r") as tar:
        #     tar.extractall(path=extract_path)
        #
        # new_file_path = os.path.join(extract_path, file_path.lstrip('/'))
        # os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
        # with open(new_file_path, 'w') as new_file:
        #     new_file.write("")  # Создаем пустой файл
        #
        # # Пересоздаем архив с новым файлом
        # with tarfile.open(self.fs_path, "w") as tar:
        #     for root, dirs, files in os.walk(extract_path):
        #         for file in files:
        #             file_full_path = os.path.join(root, file)
        #             arcname = os.path.relpath(file_full_path, extract_path)
        #             tar.add(file_full_path, arcname=arcname)
        #
        # # Удаляем временные извлеченные файлы
        # for root, dirs, files in os.walk(extract_path, topdown=False):
        #     for name in files:
        #         os.remove(os.path.join(root, name))
        #     for name in dirs:
        #         os.rmdir(os.path.join(root, name))
        #
        # return f"Файл '{filename}' создан."

    # def touch(self, filename):
    #     # Создание пустого файла или обновление времени для существующего.
    #     current_path = self.current_dir.rstrip('/') + '/' if self.current_dir != '/' else '/'
    #     file_path = current_path + filename
    #
    #     # Если файл уже существует в виртуальной файловой системе
    #     if file_path in self.fs.list_files():
    #         # Извлекаем содержимое архива
    #         extract_path = "./temp_fs"
    #         with tarfile.open(self.fs_path, "r") as tar:
    #             tar.extractall(path=extract_path)
    #
    #         # Путь к извлеченному файлу
    #         extracted_file_path = os.path.join(extract_path, file_path.lstrip('/'))
    #         print(extracted_file_path)
    #         if os.path.exists(extracted_file_path):
    #             # Обновляем временную метку
    #             os.utime(extracted_file_path, None)
    #             message = f"Метка времени для '{filename}' обновлена."
    #
    #             # Создаем новый архив с обновленными файлами
    #             with tarfile.open(self.fs_path, "w") as tar:
    #                 tar.add(extract_path, arcname="files")
    #
    #             # Удаляем временные извлеченные файлы
    #             for root, dirs, files in os.walk(extract_path, topdown=False):
    #                 for name in files:
    #                     os.remove(os.path.join(root, name))
    #                 for name in dirs:
    #                     os.rmdir(os.path.join(root, name))
    #         else:
    #             message = f"Ошибка: файл '{filename}' не найден в архиве."
    #         return message
    #
    #     # Если файл не существует, создаем пустой  файл и устанавливаем начальную метку времени
    #     self.virtual_files[file_path] = ""  # Пустое содержимое файла
    #     self.file_timestamps[file_path] = time.ctime()  # Устанавливаем текущее время как метку времени
    #     return f"Файл '{filename}' создан: {self.file_timestamps[file_path]}"

    def tac(self, filename):
        # Вывод содержимого файла, перевернутого строками.
        current_path = self.current_dir.lstrip('/') + '/' if self.current_dir != '/' else ''
        full_filename = current_path + filename

        #  if full_filename not in self.virtual_files or not self.virtual_files[full_filename]:
        #      return f"Виртуальный файл '{filename}' пуст."
        # Проверка на виртуальные файлы
        if full_filename in self.virtual_files:
            content = self.virtual_files[full_filename]
            if not content or content == '':
                return f"Виртуальный файл '{filename}' пуст."
            return '\n'.join(content.splitlines()[::-1])

        # Если файл не виртуальный, пробуем его прочитать из файловой системы
        content = self.fs.open_file(full_filename)
        check = self.fs.check_file(full_filename)
        if not check:
            return content
        else:
            return content[::-1]
        # if content.startswith("Файл"):
        #      return content

    def exit(self):
        sys.exit(0)

    def execute_script(self):
        # Чтение команд из стартового скрипта и их выполнение
        if self.script_path:
            try:
                with open(self.script_path, 'r') as script_file:
                    for line in script_file:
                        line = line.strip()  # Убираем лишние пробелы
                        if line:
                            print(f"Выполнение: {line}")
                            result = self.execute_command(line)
                            print(result)
            except FileNotFoundError:
                print(f"Ошибка: Файл стартового скрипта '{self.script_path}' не найден.")
        else:
            print("Непредоставлен стартовый скрипт.")
