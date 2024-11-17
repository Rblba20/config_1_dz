import argparse
from fs_handler import VirtualFileSystem
from gui import run_gui

def parse_args():
    parser = argparse.ArgumentParser(description="Shell emulator")
    parser.add_argument("username", help="Имя пользователя")
    parser.add_argument("fs_archive", help="Путь к tar архиву виртуальной файловой системы")
    parser.add_argument("start_script", help="Путь к стартовому скрипту")
    return parser.parse_args()

def main():
    args = parse_args()
    # Создаем объект виртуальной файловой системы
    fs = VirtualFileSystem(args.fs_archive)

    # Запускаем GUI с эмулятором оболочки
    run_gui(args.username, fs, args.fs_archive, args.start_script)

if __name__ == "__main__":
    main()



# Для запуска эмулятора из командной строки:
# python emulator.py user test_fs.tar
# python emulator.py username /path/to/fs_archive.tar /path/to/startup_script.txt
# python emulator.py username /path/to/fs_archive.tar /path/to/startup_script.txt
# python emulator.py username test_fs.tar startup_script.txt
# УБРАТЬ ОS
# tar -cvf test_fs.tar testing
# endless directories after touch