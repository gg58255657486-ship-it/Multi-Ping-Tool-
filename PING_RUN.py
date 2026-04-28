import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import multiprocessing

class PingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Ping Tool")
        self.root.geometry("300x250")

        # Поле для ввода IP
        tk.Label(root, text="Введите IP или адрес:").pack(pady=5)
        self.entry_ip = tk.Entry(root)
        self.entry_ip.insert(0, "8.8.8.8")
        self.entry_ip.pack(pady=5)

        # Поле для ввода количества окон
        tk.Label(root, text="Количество окон:").pack(pady=5)
        self.entry_count = tk.Entry(root)
        self.entry_count.insert(0, "3")
        self.entry_count.pack(pady=5)

        # Кнопка запуска
        self.btn_start = tk.Button(root, text="Запустить пинг", command=self.start_pings, bg="green", fg="white")
        self.btn_start.pack(pady=10, fill=tk.X, padx=20)

        # Кнопка закрытия
        self.btn_stop = tk.Button(root, text="Закрыть все окна", command=self.stop_pings, bg="red", fg="white")
        self.btn_stop.pack(pady=5, fill=tk.X, padx=20)

        # Уникальный заголовок
        self.window_title = "PING_PROCESS_WINDOW"

    def start_pings(self):
        ip = self.entry_ip.get().strip()
        try:
            count = int(self.entry_count.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число в поле количества окон")
            return

        if not ip:
            messagebox.showerror("Ошибка", "Введите адрес")
            return

        for i in range(count):
            # Вместо start используем явный вызов cmd.exe
            # /k - выполнить команду и оставить окно, title - задать заголовок
            # CREATE_NEW_CONSOLE - флаг Windows для запуска в новом окне
            cmd_command = f'title {self.window_title} && ping {ip} -t'
            
            try:
                subprocess.Popen(
                    ['cmd', '/k', cmd_command],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            except Exception as e:
                messagebox.showerror("Ошибка запуска", f"Не удалось запустить процесс: {e}")

    def stop_pings(self):
        # Используем taskkill для закрытия окон по заголовку
        try:
            # /F - принудительно, /FI - фильтр по заголовку, /T - дерево процессов
            os.system(f'taskkill /F /FI "WINDOWTITLE eq {self.window_title}*" /T')
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось закрыть окна: {e}")

if __name__ == "__main__":
    # Критически важно для скомпилированных EXE
    multiprocessing.freeze_support()
    
    root = tk.Tk()
    app = PingApp(root)
    root.mainloop()