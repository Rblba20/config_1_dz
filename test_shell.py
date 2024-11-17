import unittest
from fs_handler import VirtualFileSystem
from shell import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем виртуальную файловую систему для тестов
        cls.fs_archive = "test_fs.tar"
        cls.username = "test_user"
        cls.start_script = "test_script.txt"

        # Создаем виртуальный файловый архив для тестов
        cls.fs = VirtualFileSystem(cls.fs_archive)

    def setUp(self):
        # Инициализируем эмулятор для каждого теста
        self.shell = ShellEmulator(self.username, self.fs, self.fs_archive, self.start_script)

    # Тесты для команды ls
    def test_ls_root(self):
        result = self.shell.ls()
        self.assertIn("testing", result)

    def test_ls_testing(self):
        self.shell.cd("testing")
        result = self.shell.ls()
        self.assertIn("testdir", result)
        self.assertIn("testdir2", result)

    def test_ls_testdir(self):
        self.shell.cd("testing/testdir")
        result = self.shell.ls()
        self.assertIn("testfile1.txt", result)
        self.assertIn("testfile2.txt", result)
        self.assertIn("testfile3.txt", result)

    # Тесты для команды cd
    def test_cd_to_existing_dir(self):
        result = self.shell.cd("testing/testdir")
        self.assertEqual(self.shell.current_dir, "testing/testdir")
        self.assertEqual(result, "")

    def test_cd_invalid_dir(self):
        result = self.shell.cd("nonexistent")
        self.assertIn("Directory not found", result)

    def test_cd_back_to_parent(self):
        self.shell.cd("testing/testdir")
        self.shell.cd("..")
        self.assertEqual(self.shell.current_dir, "testing")

    # Тесты для команды touch
    def test_touch_create_new_file(self):
        self.shell.cd("testing/testdir")
        result = self.shell.touch("newfile.txt")
        self.assertEqual("Файл 'newfile.txt' создан", result)
        index = str(self.shell.virtual_files).find(":")
        self.assertEqual("testing/testdir/newfile.txt", str(self.shell.virtual_files)[2:index-1])

    def test_touch_update_existing_file(self):
        self.shell.cd("testing/testdir2")
        result = self.shell.touch("testfile21.txt")
        self.assertIn("Метка времени для 'testfile21.txt' обновлена.", result)

    def test_touch_nonexistent_path(self):
        self.shell.cd("nonexistent")
        result = self.shell.touch("newfile.txt")
        self.assertIn("Файл 'newfile.txt' создан", result)

    # Тесты для команды tac
    def test_tac_existing_file(self):
        self.shell.cd("testing/testdir2")
        result = self.shell.tac("testfile22.txt")
        self.assertEqual(result, "txt.22eliftset si sihT")

    def test_tac_empty_file(self):
        self.shell.cd("testing/testdir2")
        self.shell.touch("emptyfile.txt")
        result = self.shell.tac("emptyfile.txt")
        self.assertEqual(result, "Виртуальный файл 'emptyfile.txt' пуст.")

    def test_tac_nonexistent_file(self):
        self.shell.cd("testing/testdir2")
        result = self.shell.tac("nonexistent.txt")
        self.assertEqual("Файл testing/testdir2/nonexistent.txt не найден в архиве", result)

    # Тесты для команды exit
    def test_exit(self):
        with self.assertRaises(SystemExit):
            self.shell.exit()

if __name__ == "__main__":
    unittest.main()


# python -m unittest discover
# coverage run -m unittest discover
# coverage report
# coverage html