import tkinter as tk
from tkinter import ttk, messagebox
import os
import string
import random
import hashlib
from datetime import datetime


def hash_password(password):
    """Хэш пароля — для проверки без хранения в открытом виде."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class SolarAppV1:

    MIN_PASSWORD_LENGTH = 3
    TELEGRAM_TAG_HELP = "@xpon5"

    def __init__(self, root):
        self.root = root
        self.root.title("Solar App V1")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Текущий пользователь
        self.current_login = None
        self.current_password = None
        self.registered_this_session = False

        # Верхняя панель
        top_bar = ttk.Frame(self.root)
        top_bar.pack(side="top", fill="x")

        self.account_label = ttk.Label(
            top_bar, text="Гость", anchor="e", cursor="hand2"
        )
        self.account_label.pack(side="right", padx=10, pady=5)
        self.account_label.bind("<Button-1>", self.show_password)

        # Вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Статус-бар
        self.status_var = tk.StringVar(value="Готово")
        ttk.Label(
            self.root, textvariable=self.status_var, anchor="w", relief="sunken"
        ).pack(side="bottom", fill="x")

        # Создаём вкладки
        self.create_auth_tab()
        self.create_reg_tab()
        self.create_calk_tab()
        self.create_info_tab()
        self.create_password_tab()
        self.create_note_tab()
        self.create_help_tab()

    def set_status(self, text):
        self.status_var.set(text)

    # ---------------- Общая проверка пароля ----------------
    def validate_password(self, password):
        if len(password) < self.MIN_PASSWORD_LENGTH:
            return False, f"Пароль должен содержать минимум {self.MIN_PASSWORD_LENGTH} символа(ов)"
        if " " in password:
            return False, "Пароль не должен содержать пробелы"
        return True, ""

    def show_password(self, event=None):
        if not self.current_login:
            messagebox.showinfo("Аккаунт", "Вы ещё не авторизованы")
            return
        messagebox.showinfo(
            "Данные аккаунта",
            f"Логин: {self.current_login}\nПароль: {self.current_password}"
        )

    # ==================== АВТОРИЗАЦИЯ ====================

    def create_auth_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Авторизация")

        ttk.Label(frame, text="Логин:").pack(pady=10)
        self.auth_entry1 = ttk.Entry(frame)
        self.auth_entry1.pack(pady=5)

        ttk.Label(frame, text="Пароль:").pack(pady=10)
        self.auth_entry2 = ttk.Entry(frame, show="*")
        self.auth_entry2.pack(pady=5)

        ttk.Button(frame, text="Войти", command=self.login).pack(pady=10)

        if not os.path.exists("login.txt"):
            open("login.txt", "w").close()

    def login(self):
        login = self.auth_entry1.get()
        password = self.auth_entry2.get()

        if not login or not password:
            messagebox.showwarning("Ошибка", "Заполните логин и пароль")
            return

        with open("login.txt", "r", encoding="utf-8") as f:
            accounts = dict(
                line.strip().split(":", 1) for line in f if ":" in line
            )

        if accounts.get(login) != hash_password(password):
            messagebox.showwarning("Ошибка", "Неверный логин или пароль")
            self.set_status("Ошибка входа")
            return

        self.current_login = login
        self.current_password = password
        self.account_label.config(text=f"👤 {login}")
        self.set_status(f"Вход выполнен: {login}")
        messagebox.showinfo("Авторизация", f"Добро пожаловать, {login}!")

    # ==================== РЕГИСТРАЦИЯ ====================

    def create_reg_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Регистрация")

        ttk.Label(frame, text="Создать логин:").pack(pady=10)
        self.reg_entry1 = ttk.Entry(frame)
        self.reg_entry1.pack(pady=5)

        ttk.Label(frame, text="Пароль:").pack(pady=10)
        self.reg_entry2 = ttk.Entry(frame, show="*")
        self.reg_entry2.pack(pady=5)

        ttk.Label(frame, text="Повторите пароль:").pack(pady=10)
        self.reg_entry3 = ttk.Entry(frame, show="*")
        self.reg_entry3.pack(pady=5)

        self.reg_button = ttk.Button(frame, text="Зарегистрироваться", command=self.register)
        self.reg_button.pack(pady=10)

    def register(self):
        if self.registered_this_session:
            messagebox.showwarning(
                "Ограничение",
                "В этой сессии уже был зарегистрирован один аккаунт.\nПерезапустите приложение."
            )
            return

        login = self.reg_entry1.get()
        password = self.reg_entry2.get()
        password_repeat = self.reg_entry3.get()

        if not login or not password or not password_repeat:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        valid, message = self.validate_password(password)
        if not valid:
            messagebox.showwarning("Ошибка", message)
            return

        if password != password_repeat:
            messagebox.showwarning("Ошибка", "Пароли не совпадают")
            return

        with open("login.txt", "a", encoding="utf-8") as f:
            f.write(f"{login}:{hash_password(password)}\n")

        self.registered_this_session = True
        self.current_login = login
        self.current_password = password
        self.account_label.config(text=f"👤 {login}")

        self.reg_button.config(state="disabled")
        self.reg_entry1.config(state="disabled")
        self.reg_entry2.config(state="disabled")
        self.reg_entry3.config(state="disabled")

        self.set_status(f"Зарегистрирован новый пользователь: {login}")
        messagebox.showinfo("Регистрация", f"Пользователь {login} зарегистрирован!")

    # ==================== КАЛЬКУЛЯТОР ====================

    def create_calk_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Калькулятор")

        ttk.Label(frame, text="Введите первое число:").pack(pady=5)
        self.calk_entry1 = ttk.Entry(frame)
        self.calk_entry1.pack(pady=5)

        ttk.Label(frame, text="Выберите операцию:").pack(pady=5)
        self.operation_var = tk.StringVar(value="+")
        self.operation_combo = ttk.Combobox(
            frame,
            textvariable=self.operation_var,
            values=["+", "-", "*", "/"],
            state="readonly",
            justify="center",
            width=10
        )
        self.operation_combo.pack(pady=5)

        ttk.Label(frame, text="Введите второе число:").pack(pady=5)
        self.calk_entry3 = ttk.Entry(frame)
        self.calk_entry3.pack(pady=5)

        ttk.Button(frame, text="Посчитать", command=self.calculate).pack(pady=10)

        self.calk_result = ttk.Label(frame, text="Результат:")
        self.calk_result.pack(pady=10)

    def calculate(self):
        operations = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }

        try:
            num1 = float(self.calk_entry1.get())
            operation = self.operation_var.get()
            num2 = float(self.calk_entry3.get())
        except ValueError:
            messagebox.showwarning("Ошибка", "Введите числа правильно")
            return

        if operation not in operations:
            messagebox.showwarning("Ошибка", "Используйте только + - * /")
            return

        if operation == "/" and num2 == 0:
            messagebox.showwarning("Ошибка", "На ноль делить нельзя")
            return

        result = operations[operation](num1, num2)
        self.calk_result.config(text=f"Результат: {result}")
        messagebox.showinfo("Результат", f"Ответ: {result}")

    # ==================== ГЕНЕРАЦИЯ ПАРОЛЯ ====================

    def create_password_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Генерация пароля")

        ttk.Label(frame, text="Длина пароля:").pack(pady=(15, 0))
        self.length_var = tk.StringVar(value="12")
        ttk.Entry(frame, textvariable=self.length_var).pack()

        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        options_frame = ttk.Frame(frame)
        options_frame.pack(pady=12)

        ttk.Checkbutton(options_frame, text="Заглавные (A-Z)", variable=self.use_upper).pack(anchor="w")
        ttk.Checkbutton(options_frame, text="Строчные (a-z)", variable=self.use_lower).pack(anchor="w")
        ttk.Checkbutton(options_frame, text="Цифры (0-9)", variable=self.use_digits).pack(anchor="w")
        ttk.Checkbutton(options_frame, text="Символы (!@#...)", variable=self.use_symbols).pack(anchor="w")

        ttk.Button(frame, text="Сгенерировать", command=self.generate_password).pack(pady=10)

        self.password_var = tk.StringVar()
        ttk.Entry(
            frame, textvariable=self.password_var, justify="center", font=("Consolas", 12)
        ).pack(pady=5, fill="x", padx=20)

    def generate_password(self):
        try:
            length = int(self.length_var.get())
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Длина пароля должна быть целым числом.")
            return

        if length <= 0:
            messagebox.showerror("Ошибка ввода", "Длина пароля должна быть больше нуля.")
            return

        if length >= 100:
            messagebox.showerror("Ошибка", "Максимальная длинна 100 символов!")
            return

        characters = ""
        if self.use_upper.get():
            characters += string.ascii_uppercase
        if self.use_lower.get():
            characters += string.ascii_lowercase
        if self.use_digits.get():
            characters += string.digits
        if self.use_symbols.get():
            characters += string.punctuation

        if not characters:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов.")
            return

        password = "".join(random.choice(characters) for _ in range(length))
        self.password_var.set(password)

    # ==================== ЗАМЕТКИ ====================

    def create_note_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Заметки")

        ttk.Label(frame, text="Заметки:").pack(pady=5)

        self.note_text = tk.Text(frame, wrap="word", height=12)
        self.note_text.pack(pady=10, padx=10, fill="both", expand=True)

        note_buttons = ttk.Frame(frame)
        note_buttons.pack(pady=(0, 5))

        ttk.Button(note_buttons, text="Сохранить", command=self.save_note).pack(side="left", padx=5)
        ttk.Button(note_buttons, text="Очистить", command=self.clear_note).pack(side="left", padx=5)

        ttk.Label(frame, text="Сохранённые заметки:").pack(pady=(10, 0))

        list_frame = ttk.Frame(frame)
        list_frame.pack(pady=5, padx=10, fill="both")

        self.notes_listbox = tk.Listbox(list_frame, height=6)
        self.notes_listbox.pack(side="left", fill="both", expand=True)

        list_buttons = ttk.Frame(list_frame)
        list_buttons.pack(side="left", padx=5)

        ttk.Button(list_buttons, text="Обновить", command=self.refresh_notes_list).pack(pady=2, fill="x")
        ttk.Button(list_buttons, text="Открыть", command=self.open_selected_note).pack(pady=2, fill="x")
        ttk.Button(list_buttons, text="Удалить", command=self.delete_selected_note).pack(pady=2, fill="x")

        self.refresh_notes_list()

    def get_notes_dir(self):
        notes_dir = os.path.join(os.path.expanduser("~"), "SolarApp_Notes")
        os.makedirs(notes_dir, exist_ok=True)
        return notes_dir

    def clear_note(self):
        self.note_text.delete("1.0", "end")
        self.set_status("Поле заметки очищено")

    def refresh_notes_list(self):
        self.notes_listbox.delete(0, "end")
        notes_dir = self.get_notes_dir()
        for filename in sorted(os.listdir(notes_dir), reverse=True):
            self.notes_listbox.insert("end", filename)

    def open_selected_note(self):
        selection = self.notes_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Сначала выберите заметку в списке")
            return

        filename = self.notes_listbox.get(selection[0])
        filepath = os.path.join(self.get_notes_dir(), filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        self.note_text.delete("1.0", "end")
        self.note_text.insert("1.0", content)
        self.set_status(f"Открыта заметка: {filename}")

    def delete_selected_note(self):
        selection = self.notes_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Сначала выберите заметку в списке")
            return

        filename = self.notes_listbox.get(selection[0])
        if not messagebox.askyesno("Удаление", f"Удалить заметку «{filename}» навсегда?"):
            return

        os.remove(os.path.join(self.get_notes_dir(), filename))
        self.refresh_notes_list()
        self.set_status(f"Заметка удалена: {filename}")

    def save_note(self):
        text = self.note_text.get("1.0", "end").strip()

        if not text:
            messagebox.showwarning("Ошибка", "Заметка пустая, нечего сохранять")
            return

        filename = datetime.now().strftime("note_%Y-%m-%d_%H-%M-%S.txt")
        filepath = os.path.join(self.get_notes_dir(), filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)

        self.refresh_notes_list()
        self.set_status(f"Заметка сохранена: {filename}")
        messagebox.showinfo("Заметка сохранена", f"Файл создан:\n{filepath}")

    # ==================== ИНФОРМАЦИЯ ====================

    def create_info_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Информация")

        ttk.Label(frame, text="Информация:").pack(pady=10)

        info_text = tk.Text(frame, wrap="word", height=15)
        info_text.insert(
            "1.0",
            "Данное приложение находится в Альфа-тесте.\n"
            "Создано 15.09.2026 учеником 7А класса.\n"
            "*С использованием ИИ*\n"
            "___________________________________\n"
            "Версия 1.0.16 ALFA\n"
            "Политики:\n"
            "1. Мы не собираем ваши данные. Все файлы хранятся локально на вашем устройстве!\n"
            "___________________________________\n"
            "Обновления:\n"
            "1.0.15-Обновление Генерации пароля теперь максимальная длинна до 100 символов\n"
            "1.0.16-Обновление операций в калькуляторе:Добавлен новый выбор операций,оптимизация функций и кода"
        )
        info_text.config(state="disabled")
        info_text.pack(pady=10, padx=10, fill="both", expand=True)

    # ==================== ТЕХ. ПОДДЕРЖКА ====================

    def create_help_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Тех. Поддержка")

        ttk.Label(frame, text="Тех. Поддержка").pack(pady=5)
        ttk.Label(frame, text="Telegram:").pack(pady=5)

        help_entry = ttk.Entry(frame, justify="center")
        help_entry.insert(0, self.TELEGRAM_TAG_HELP)
        help_entry.config(state="readonly")
        help_entry.pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = SolarAppV1(root)
    root.mainloop()