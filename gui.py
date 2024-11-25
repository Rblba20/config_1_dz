import tkinter as tk
from tkinter import scrolledtext
from shell import ShellEmulator
from fs_handler import VirtualFileSystem


class ShellGUI:
    def __init__(self, shell):
        self.shell = shell
        self.root = tk.Tk()
        self.root.title("Shell Emulator")
        self.root.configure(bg="black")

        # Настройка текстового вывода
        self.text_output = scrolledtext.ScrolledText(
            self.root,
            bg="black",
            fg="green",
            insertbackground="green",
            font=("Consolas", 12),
            wrap=tk.WORD,
        )
        self.text_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        # Поле ввода команды
        self.entry_input = tk.Entry(
            self.root,
            bg="black",
            fg="green",
            insertbackground="green",
            font=("Consolas", 12),
        )
        self.entry_input.pack(fill=tk.X, padx=10, pady=(0, 5))
        self.entry_input.bind("<Return>", self.process_command)

        # Кнопки управления
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        self.clear_button = tk.Button(
            button_frame,
            text="Очистить экран",
            command=self.clear_output,
            bg="gray",
            fg="black",
            font=("Consolas", 10, "bold"),
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(
            button_frame,
            text="Выход",
            command=self.root.quit,
            bg="gray",
            fg="black",
            font=("Consolas", 10, "bold"),
        )
        self.exit_button.pack(side=tk.RIGHT, padx=5)

    def process_command(self, event):
        command = self.entry_input.get()
        self.entry_input.delete(0, tk.END)
        self.text_output.insert(tk.END, f"{self.shell.prompt()}{command}\n")
        self.text_output.see(tk.END)  # Прокрутка вниз
        output = self.shell.execute_command(command)
        if output:
            self.text_output.insert(tk.END, f"{output}\n")
            self.text_output.see(tk.END)  # Прокрутка вниз

    def clear_output(self):
        self.text_output.delete("1.0", tk.END)

    def start(self):
        self.root.mainloop()


def run_gui(username, fs, fs_archive, start_script):
    shell = ShellEmulator(username, fs, fs_archive, start_script)
    gui = ShellGUI(shell)

    # Выполняем стартовый скрипт и записываем результат в GUI
    output = shell.execute_script()
    if output:
        gui.text_output.insert(tk.END, f"{output}\n")
        gui.text_output.see(tk.END)  # Прокрутка вниз

    gui.start()


# def run_gui(username, fs, fs_archive, start_script):
#     shell = ShellEmulator(username, fs, fs_archive, start_script)
#     shell.execute_script()
#     gui = ShellGUI(shell)
#     gui.start()
