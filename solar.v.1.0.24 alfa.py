import tkinter as tk
from tkinter import ttk, messagebox
import os
import tempfile
import time
import string
import random
import hashlib
from datetime import datetime
import requests
import threading

VERS = "1.0.24ALFA"

_logo_lines = [
    "███████╗ ██████╗ ██╗      █████╗ ██████╗      █████╗ ██████╗ ██████╗ ",
    "██╔════╝██╔═══██╗██║     ██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔══██╗",
    "███████╗██║   ██║██║     ███████║██████╔╝    ███████║██████╔╝██████╔╝",
    "╚════██║██║   ██║██║     ██╔══██║██╔══██╗    ██╔══██║██╔═══╝ ██╔═══╝ ",
    "███████║╚██████╔╝███████╗██║  ██║██║  ██║    ██║  ██║██║     ██║     ",
    "╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝     ╚═╝     ",
    VERS,
]
_signature = "by dfsaetg"

_inner = max(len(l) for l in _logo_lines + [_signature]) + 4


def _row(text=""):
    return "║" + text.center(_inner) + "║"


_banner_lines = ["╔" + "═" * _inner + "╗", _row()]
for _l in _logo_lines:
    _banner_lines.append(_row(_l))
_banner_lines.append(_row())
_banner_lines.append(_row(_signature))
_banner_lines.append(_row())
_banner_lines.append("╚" + "═" * _inner + "╝")

_status_path = os.path.join(tempfile.gettempdir(), "solar_status.txt")

_ps = []
_ps.append('$Host.UI.RawUI.WindowTitle = "SOLAR APP"')
_ps.append('Clear-Host')
_ps.append('Write-Host ""')
_ps.append('Write-Host "     [ Нажмите ENTER для пропуска анимации ]" -ForegroundColor DarkRed')
_ps.append('Write-Host ""')
_ps.append('Start-Sleep -Milliseconds 1200')
_ps.append('Clear-Host')
_ps.append('$skip = $false')
_ps.append('$statusFile = "' + _status_path + '"')
_ps.append('$lines = @(')
_ps.append(",\n".join('    "' + l + '"' for l in _banner_lines))
_ps.append(')')
_ps.append('')
_ps.append('if ([Console]::KeyAvailable) {')
_ps.append('    $k = [Console]::ReadKey($true)')
_ps.append('    if ($k.Key -eq "Enter") { $skip = $true }')
_ps.append('}')
_ps.append('')
_ps.append('if (-not $skip) {')
_ps.append('    :outer foreach ($line in $lines) {')
_ps.append('        foreach ($ch in $line.ToCharArray()) {')
_ps.append('            if ([Console]::KeyAvailable) {')
_ps.append('                $k = [Console]::ReadKey($true)')
_ps.append('                if ($k.Key -eq "Enter") { $skip = $true; break outer }')
_ps.append('            }')
_ps.append('            Write-Host -NoNewline $ch -ForegroundColor Red')
_ps.append('            Start-Sleep -Milliseconds 8')
_ps.append('        }')
_ps.append('        Write-Host ""')
_ps.append('    }')
_ps.append('}')
_ps.append('')
_ps.append('if ($skip) {')
_ps.append('    Clear-Host')
_ps.append('    foreach ($line in $lines) { Write-Host $line -ForegroundColor Red }')
_ps.append('    Write-Host ""')
_ps.append('    Write-Host "     [ Анимация пропущена ]" -ForegroundColor DarkRed')
_ps.append('    Start-Sleep -Seconds 2')
_ps.append('    Set-Content -Path $statusFile -Value "skip" -Encoding UTF8')
_ps.append('} else {')
_ps.append('    Start-Sleep -Seconds 10')
_ps.append('    Set-Content -Path $statusFile -Value "done" -Encoding UTF8')
_ps.append('}')

_ps_script = "\n".join(_ps)

_ps_path = os.path.join(tempfile.gettempdir(), "solar_banner.ps1")
with open(_ps_path, "w", encoding="utf-8-sig") as f:
    f.write(_ps_script)

_bat = (
    "@echo off\r\n"
    "chcp 65001 >nul\r\n"
    "color 0C\r\n"
    "title SOLAR APP\r\n"
    'powershell -NoProfile -ExecutionPolicy Bypass -File "' + _ps_path + '"\r\n'
    "exit\r\n"
)
_bat_path = os.path.join(tempfile.gettempdir(), "solar_banner.bat")
with open(_bat_path, "w", encoding="utf-8") as f:
    f.write(_bat)

if os.path.exists(_status_path):
    os.remove(_status_path)

os.system('start "" cmd /c "' + _bat_path + '"')

_deadline = time.time() + 16
while time.time() < _deadline:
    if os.path.exists(_status_path):
        break
    time.sleep(0.1)


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class SolarAppV1_1:

    MIN_PASSWORD_LENGTH = 3
    TELEGRAM_TAG_HELP = "@xpon5"
    GITHUB = "https://github.com/farmaphik/Solar-app"
    TIKTOK = "https://tiktok.com/@solar_app"
    DISCORD = "https://discord.gg/hfMMPYBVUu"

    CURRENCY_CODES = {
        "USD": "Доллар",
        "EUR": "Евро",
        "RUB": "Рубль",
        "KZT": "Тенге",
        "UAH": "Гривна",
        "GBP": "Фунт стерлингов",
        "CNY": "Юань",
        "TRY": "Турецкая лира",
        "GEL": "Лари",
        "BYN": "Белорусский рубль",
        "KGS": "Сом",
        "UZS": "Сум",
        "CHF": "Франк",
        "JPY": "Иена",
    }

    WEATHER_CITIES = [
        
    "Алматы", "Астана", "Усть-Каменогорск", "Семей",
    "Павлодар", "Караганда", "Шымкент", "Тараз",
    "Костанай", "Петропавловск", "Кокшетау", "Актобе",
    "Актау", "Атырау", "Талдыкорган", "Туркестан",
    "Риддер", "Экибастуз", "Рудный", "Жезказган",
    "Балхаш", "Кызылорда", "Уральск", "Жанаозен",
    "Сатпаев", "Темиртау",
 
    "Москва", "Санкт-Петербург", "Новосибирск",
    "Екатеринбург", "Казань", "Самара", "Омск",
    "Красноярск", "Владивосток", "Сочи",
    "Нижний Новгород", "Челябинск", "Уфа", "Волгоград",
    "Пермь", "Ростов-на-Дону", "Воронеж", "Тюмень",
    "Краснодар", "Ижевск", "Барнаул", "Ульяновск",
    "Иркутск", "Хабаровск", "Ярославль", "Томск",
    "Оренбург", "Кемерово", "Рязань", "Набережные Челны",
    "Астрахань", "Пенза", "Липецк", "Тольятти",
    "Киров", "Чебоксары", "Калининград", "Брянск",
    "Курск", "Магнитогорск", "Тверь", "Ставрополь",
    "Белгород", "Сургут", "Владимир", "Архангельск",
    "Мурманск", "Якутск", "Петрозаводск", "Норильск",
 
    "Киев", "Минск", "Ташкент", "Бишкек",
    "Душанбе", "Баку", "Ереван", "Тбилиси",
    "Харьков", "Одесса", "Львов", "Днепр",
    "Гомель", "Могилёв", "Витебск", "Самарканд",
    "Бухара", "Нукус", "Ош", "Худжанд",
    "Гянджа", "Батуми", "Кутаиси", "Сухум",
    "Ашхабад", "Кишинёв", "Тирасполь",
 
    "Лондон", "Париж", "Берлин", "Рим",
    "Мадрид", "Амстердам", "Прага", "Варшава",
    "Вена", "Будапешт", "Брюссель", "Цюрих",
    "Женева", "Милан", "Барселона", "Лиссабон",
    "Дублин", "Копенгаген", "Стокгольм", "Осло",
    "Хельсинки", "Афины", "Белград", "Загреб",
    "Братислава", "Любляна", "Вильнюс", "Рига",
    "Таллин", "Мюнхен", "Гамбург", "Кёльн",
    "Франкфурт", "Неаполь", "Венеция", "Флоренция",
    "Севилья", "Валенсия", "Роттердам", "Антверпен",
    "Краков", "Гданьск", "Вроцлав", "Бухарест",
    "София", "Ницца", "Марсель", "Лион",
    "Эдинбург", "Манчестер", "Глазго", "Порту",
 
    "Стамбул", "Анкара", "Измир", "Дубай",
    "Абу-Даби", "Каир", "Токио", "Осака",
    "Киото", "Сеул", "Пусан", "Пекин",
    "Шанхай", "Гуанчжоу", "Шэньчжэнь", "Гонконг",
    "Сингапур", "Куала-Лумпур", "Джакарта", "Манила",
    "Ханой", "Хошимин", "Бангкок", "Дели",
    "Мумбаи", "Бангалор", "Ченнаи", "Калькутта",
    "Исламабад", "Карачи", "Лахор", "Тегеран",
    "Эр-Рияд", "Доха", "Кувейт", "Манама",
    "Бейрут", "Амман", "Иерусалим", "Тель-Авив",
 
    "Йоханнесбург", "Кейптаун", "Найроби", "Лагос",
    "Аддис-Абеба", "Касабланка", "Тунис", "Алжир",
    "Аккра",
 
    "Нью-Йорк", "Лос-Анджелес", "Чикаго",
    "Торонто", "Ванкувер", "Мехико",
    "Вашингтон", "Бостон", "Майами", "Сан-Франциско",
    "Сиэтл", "Хьюстон", "Даллас", "Монреаль",
    "Оттава", "Гвадалахара", "Буэнос-Айрес", "Сан-Паулу",
    "Рио-де-Жанейро", "Богота", "Лима", "Сантьяго",
    "Каракас", "Кито", "Гавана",
 
    "Сидней", "Мельбурн", "Окленд",
    "Брисбен", "Перт", "Веллингтон", "Крайстчерч",
]

    def __init__(self, root):
        self.root = root
        self.root.title("Solar App " + VERS)
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        self.current_login = None
        self.current_password = None
        self.registered_this_session = False
        self.rate_cache = {}
        self.Create_data = None
        self.calk_history = []
        
        top_bar = ttk.Frame(self.root)
        top_bar.pack(side="top", fill="x")

        top_bar1 = ttk.Frame(self.root)
        top_bar1.pack(side="top", fill="x")

        top_bar2 = ttk.Frame(self.root)
        top_bar2.pack(side="top", fill="x")

        self.account_label = ttk.Label(top_bar, text="Гость", anchor="e", cursor="hand2")
        self.account_label.pack(side="right", padx=10, pady=5)
        self.account_label.bind("<Button-1>", self.show_password)

        self.account_label1 = ttk.Label(top_bar1, text="Выйти из аккаунта")
        self.account_label1.pack(side="right", padx=10, pady=5)
        self.account_label1.bind("<Button-1>", self.exit)

        self.pogoda_label = ttk.Label(top_bar2, text="Погода  ",
                              cursor="hand2", foreground="blue")
        self.pogoda_label.pack(side="left", padx=5, pady=5)
        self.pogoda_label.bind("<Button-1>", self.open_city_menu)

        # Раньше этого лейбла не было в коде вообще, хотя fetch_city_weather
        # на него ссылался -> при выборе города падал AttributeError.
        self.mini_pogoda_label = ttk.Label(top_bar2, text="")
        self.mini_pogoda_label.pack(side="left", padx=5, pady=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.status_var = tk.StringVar(value="Готово")
        ttk.Label(self.root, textvariable=self.status_var, anchor="w", relief="sunken").pack(side="bottom", fill="x")

        self.create_auth_tab()
        self.create_reg_tab()
        self.create_calk_tab()
        self.create_password_tab()
        self.create_note_tab()
        self.create_cred_tab()
        self.create_time_tab()
        self.create_conv_tab()
        self.create_pogoda_tab()
        self.create_help_tab()
        self.create_info_tab()

    def exit(self, event=None):
        if not self.current_login:
            messagebox.showinfo("Аккаунт", "Вы ещё не авторизованы")
            return

        login = self.current_login
        self.current_login = None
        self.current_password = None
        self.Create_data = None
        self.account_label.config(text="Гость")

        self.set_status(f"Вы вышли из аккаунта: {login}")
        messagebox.showinfo("Аккаунт", f"Вы вышли из аккаунта! {login}")

    def set_status(self, text):
        self.status_var.set(text)

    def validate_password(self, password):
        if len(password) < self.MIN_PASSWORD_LENGTH:
            return False, f"Пароль должен содержать минимум {self.MIN_PASSWORD_LENGTH} символа"
        if " " in password:
            return False, "Пароль не должен содержать пробелы"
        return True, ""

    def show_password(self, event=None):
        if not self.current_login:
            messagebox.showinfo("Аккаунт", "Вы ещё не авторизованы")
            return
        created = self.Create_data if self.Create_data else "неизвестно"
        messagebox.showinfo(
            "Данные аккаунта",
            f"Логин: {self.current_login}\n"
            f"Пароль: {self.current_password}\n"
            f"Дата создания: {created}"
        )

    # -------------------- МИНИ-ПОГОДА ВВЕРХУ --------------------

    def open_city_menu(self, event=None):
        menu = tk.Menu(self.root, tearoff=0)
        for city in self.WEATHER_CITIES:
            menu.add_command(label=city,
                             command=lambda c=city: self.show_city_weather(c))

        if event is not None:
            menu.post(event.x_root, event.y_root)
        else:
            menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def show_city_weather(self, city):
        self.mini_pogoda_label.config(text="Загрузка...")
        threading.Thread(target=self.fetch_city_weather,
                         args=(city,), daemon=True).start()

    def fetch_city_weather(self, city):
        url = f"https://wttr.in/{city}?format=j1&lang=ru"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            current = data["current_condition"][0]

            short = f"{city}: {current['temp_C']}°C, {current['lang_ru'][0]['value']}"

            full = (
                f"Город: {city}\n"
                f"Температура: {current['temp_C']}°C\n"
                f"Ощущается: {current['FeelsLikeC']}°C\n"
                f"Погода: {current['lang_ru'][0]['value']}\n"
                f"Влажность: {current['humidity']}%\n"
                f"Ветер: {current['winddir16Point']} {current['windspeedKmph']} км/ч\n"
                f"Давление: {current['pressure']} гПа"
            )

            self.mini_pogoda_label.config(text=short)
            messagebox.showinfo("Погода", full)

        except Exception as error:
            self.mini_pogoda_label.config(text="Ошибка загрузки")
            messagebox.showerror("Ошибка", f"Не удалось получить погоду:\n{error}")

    # -------------------- ВКЛАДКА ПОГОДЫ --------------------

    def create_pogoda_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Погода")

        ttk.Label(frame, text="Погода", font=("", 14, "bold")).pack(pady=10)

        ttk.Label(frame, text="Введите город:").pack()
        self.weather_city = ttk.Entry(frame, width=25, justify="center")
        self.weather_city.pack(pady=5)
        self.weather_city.insert(0, "Алматы")

        ttk.Button(frame, text="Узнать погоду",
                   command=self.get_weather).pack(pady=10)

        self.weather_text = tk.Text(frame, height=18, width=50,
                                    font=("Consolas", 11), state="disabled")
        self.weather_text.pack(pady=10, padx=10, fill="both", expand=True)

    def find_known_city(self, raw_city):
        raw_city = raw_city.strip()
        for known_city in self.WEATHER_CITIES:
            if known_city.lower() == raw_city.lower():
                return known_city
        return None

    def get_weather(self):
        raw_city = self.weather_city.get().strip()

        if not raw_city:
            messagebox.showwarning("Ошибка", "Введите название города")
            return

        city = self.find_known_city(raw_city)
        if city is None:
            messagebox.showwarning(
                "Город не найден",
                f"«{raw_city}» нет в списке поддерживаемых городов.\n"
                "Выберите город из списка (кнопка «Погода» сверху) "
                "или введите его название точно так же."
            )
            return

        self.weather_text.config(state="normal")
        self.weather_text.delete("1.0", "end")
        self.weather_text.insert("end", "Загрузка...\n")
        self.weather_text.config(state="disabled")
        self.set_status("Запрос погоды: " + city)

        threading.Thread(target=self.load_weather,
                         args=(city,), daemon=True).start()

    def load_weather(self, city):
        url = f"https://wttr.in/{city}?format=j1&lang=ru"

        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            current = data["current_condition"][0]
            today = data["weather"][0]

            text = (
                "=== СЕЙЧАС ===\n"
                f"Город: {city}\n"
                f"Температура: {current['temp_C']}°C\n"
                f"Ощущается: {current['FeelsLikeC']}°C\n"
                f"Погода: {current['lang_ru'][0]['value']}\n"
                f"Влажность: {current['humidity']}%\n"
                f"Ветер: {current['winddir16Point']} {current['windspeedKmph']} км/ч\n"
                f"Давление: {current['pressure']} гПа\n"
                f"Видимость: {current['visibility']} км\n"
                f"UV-индекс: {current['uvIndex']}\n"
            )

            text += "\n=== БЛИЖАЙШЕЕ ВРЕМЯ ===\n"
            for hour in today["hourly"][:4]:
                raw = hour["time"].zfill(4)
                formatted = raw[:2] + ":" + raw[2:]
                text += f"{formatted}   {hour['tempC']}°C   {hour['lang_ru'][0]['value']}\n"

        except Exception as error:
            text = "Не удалось получить погоду.\n" + str(error)

        self.weather_text.config(state="normal")
        self.weather_text.delete("1.0", "end")
        self.weather_text.insert("end", text)
        self.weather_text.config(state="disabled")
        self.set_status("Погода получена: " + city)

    # -------------------- АВТОРИЗАЦИЯ --------------------

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

        accounts = {}
        with open("login.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":", 2)
                if len(parts) == 2:
                    accounts[parts[0]] = (parts[1], "неизвестно")
                elif len(parts) == 3:
                    accounts[parts[0]] = (parts[1], parts[2])

        stored = accounts.get(login)
        if not stored or stored[0] != hash_password(password):
            messagebox.showwarning("Ошибка", "Неверный логин или пароль")
            self.set_status("Ошибка входа")
            return

        self.current_login = login
        self.current_password = password
        self.Create_data = stored[1]
        self.account_label.config(text=f"👤 {login}")
        self.set_status(f"Вход выполнен: {login}")
        messagebox.showinfo("Авторизация", f"С возвращением, {login}!")

    # -------------------- РАСЧЁТ СРЕДНЕЙ СУММЫ --------------------

    def create_cred_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Р. Средней суммы")

        ttk.Label(frame, text="Выберите что будете считать:").pack(pady=10)
        self.cred_var = tk.StringVar(value="Среднее трат")
        self.cred_combo = ttk.Combobox(frame, textvariable=self.cred_var,
                                        values=["Среднее трат", "Среднее зп", "Среднее чисел"],
                                        state="readonly", justify="center", width=20)
        self.cred_combo.pack(pady=5)

        ttk.Label(frame, text="Введите числа через запятую (например: 100, 250.5, 99):").pack(pady=(15, 0))
        self.cred_entry = ttk.Entry(frame, width=40, justify="center")
        self.cred_entry.pack(pady=5)

        ttk.Button(frame, text="Посчитать", command=self.calculate_average).pack(pady=15)

        self.cred_result = ttk.Label(frame, text="Результат:", font=("", 11, "bold"))
        self.cred_result.pack(pady=5)

        self.cred_details = ttk.Label(frame, text="")
        self.cred_details.pack(pady=5)

    def calculate_average(self):
        raw_text = self.cred_entry.get().strip()

        if not raw_text:
            messagebox.showwarning("Ошибка", "Введите хотя бы одно число")
            return

        parts = [p.strip() for p in raw_text.split(",") if p.strip()]

        numbers = []
        for part in parts:
            try:
                numbers.append(float(part.replace(",", ".")))
            except ValueError:
                messagebox.showwarning("Ошибка", f"«{part}» не является числом")
                return

        if not numbers:
            messagebox.showwarning("Ошибка", "Не удалось распознать ни одного числа")
            return

        if len(numbers) > 500:
            messagebox.showerror("Ошибка", "Слишком много значений, максимум 500!")
            return

        mode = self.cred_var.get()
        if mode == "Среднее трат":
            label_text = "трат"
        elif mode == "Среднее зп":
            label_text = "зарплаты"
        else:
            label_text = "чисел"

        total = sum(numbers)
        count = len(numbers)
        average = total / count

        self.cred_result.config(text=f"Среднее {label_text}: {average:.2f}")
        self.cred_details.config(
            text=f"Сумма: {total:.2f}   Количество: {count}   Мин: {min(numbers):.2f}   Макс: {max(numbers):.2f}"
        )
        self.set_status(f"Расчёт выполнен: {count} значений, среднее {average:.2f}")
        messagebox.showinfo(
            "Результат",
            f"Среднее {label_text}: {average:.2f}\n"
            f"Сумма: {total:.2f}\n"
            f"Количество: {count}\n"
            f"Мин: {min(numbers):.2f}   Макс: {max(numbers):.2f}"
        )

    # -------------------- РЕГИСТРАЦИЯ --------------------

    def create_reg_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Рег.")

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
            messagebox.showwarning("Ограничение",
                                   "В этой сессии уже был зарегистрирован один аккаунт.\nПерезапустите приложение.")
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

        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("login.txt", "a", encoding="utf-8") as f:
            f.write(f"{login}:{hash_password(password)}:{created}\n")

        self.registered_this_session = True
        self.current_login = login
        self.current_password = password
        self.Create_data = created
        self.account_label.config(text=f"👤 {login}")

        self.reg_button.config(state="disabled")
        self.reg_entry1.config(state="disabled")
        self.reg_entry2.config(state="disabled")
        self.reg_entry3.config(state="disabled")

        self.set_status(f"Зарегистрирован новый пользователь: {login}")
        messagebox.showinfo("Регистрация", f"Аккаунт {login} успешно создан!")

    # -------------------- КАЛЬКУЛЯТОР --------------------

    def create_calk_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Кальк.")

        ttk.Label(frame, text="Введите первое число:").pack(pady=5)
        self.calk_entry1 = ttk.Entry(frame)
        self.calk_entry1.pack(pady=5)

        ttk.Label(frame, text="Выберите операцию:").pack(pady=5)
        self.operation_var = tk.StringVar(value="+")
        self.operation_combo = ttk.Combobox(frame, textvariable=self.operation_var,
                                            values=["+", "-", "*", "/", "**", "//"],
                                            state="readonly", justify="center", width=10)
        self.operation_combo.pack(pady=5)

        ttk.Label(frame, text="Введите второе число:").pack(pady=5)
        self.calk_entry3 = ttk.Entry(frame)
        self.calk_entry3.pack(pady=5)

        ttk.Button(frame, text="Посчитать", command=self.calculate).pack(pady=10)

        self.calk_result = ttk.Label(frame, text="Результат:")
        self.calk_result.pack(pady=10)

        ttk.Button(frame, text="Открыть историю",
                   command=self.show_history).pack(pady=5)

        ttk.Button(frame, text="Очистить историю",
                   command=self.clear_history).pack(pady=5)

    def calculate(self):
        operations = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "**": lambda a, b: a ** b,
            "//": lambda a, b: a // b,
        }

        try:
            num1 = float(self.calk_entry1.get())
            num2 = float(self.calk_entry3.get())
        except ValueError:
            messagebox.showwarning("Ошибка", "Введите числа правильно")
            return

        operation = self.operation_var.get()
        if operation not in operations:
            messagebox.showwarning("Ошибка", "Используйте только + - * / ** //")
            return

        if operation in ("/", "//") and num2 == 0:
            messagebox.showwarning("Ошибка", "На ноль делить нельзя")
            return

        try:
            result = operations[operation](num1, num2)
        except (ValueError, OverflowError) as error:
            messagebox.showwarning("Ошибка", f"Не удалось вычислить: {error}")
            return

        self.calk_result.config(text=f"Результат: {result}")

        zapis = f"{num1} {operation} {num2} = {result}"
        self.calk_history.append(zapis)

        messagebox.showinfo("Результат", f"Ответ: {result}")

    def show_history(self):
        if not self.calk_history:
            messagebox.showinfo("История", "Пока ничего не считали")
            return

        text = ""
        for i, z in enumerate(self.calk_history, start=1):
            text = text + f"{i}) {z}\n"

        messagebox.showinfo("История вычислений", text)

    def clear_history(self):
        if not self.calk_history:
            messagebox.showinfo("История", "История и так пустая")
            return

        otvet = messagebox.askyesno("Очистка", "Точно удалить всю историю?")
        if otvet:
            self.calk_history.clear()
            messagebox.showinfo("История", "История очищена")

    # -------------------- ГЕНЕРАЦИЯ ПАРОЛЯ --------------------

    def create_password_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Г. Паролей")

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
        ttk.Entry(frame, textvariable=self.password_var, justify="center",
                  font=("Consolas", 12)).pack(pady=5, fill="x", padx=20)

    def generate_password(self):
        try:
            length = int(self.length_var.get())
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Длина пароля должна быть целым числом.")
            return

        if length <= 0:
            messagebox.showerror("Ошибка ввода", "Длина пароля должна быть больше нуля.")
            return

        if length >= 101:
            messagebox.showerror("Ошибка", "Максимальная длина 100 символов!")
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

    # -------------------- ТАЙМЕР --------------------

    def create_time_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Таймер")

        ttk.Label(frame, text="Таймер обратного отсчёта", font=("", 12, "bold")).pack(pady=15)

        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=5)

        ttk.Label(input_frame, text="Минуты:").grid(row=0, column=0, padx=5)
        self.timer_minutes_var = tk.StringVar(value="0")
        ttk.Entry(input_frame, textvariable=self.timer_minutes_var, width=5).grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Секунды:").grid(row=0, column=2, padx=5)
        self.timer_seconds_var = tk.StringVar(value="30")
        ttk.Entry(input_frame, textvariable=self.timer_seconds_var, width=5).grid(row=0, column=3, padx=5)

        self.timer_display = ttk.Label(frame, text="00:00", font=("Consolas", 32))
        self.timer_display.pack(pady=20)

        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Старт", command=self.start_timer).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Пауза", command=self.pause_timer).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Сброс", command=self.reset_timer).pack(side="left", padx=5)

        self.timer_remaining = 0
        self.timer_running = False
        self.timer_job = None

    def start_timer(self):
        if self.timer_running:
            return

        if self.timer_remaining <= 0:
            try:
                minutes = int(self.timer_minutes_var.get())
                seconds = int(self.timer_seconds_var.get())
            except ValueError:
                messagebox.showwarning("Ошибка", "Введите целые числа для минут и секунд")
                return

            if minutes < 0 or seconds < 0:
                messagebox.showwarning("Ошибка", "Время не может быть отрицательным")
                return

            if minutes >= 999:
                messagebox.showerror("Ошибка", "Больше 999 минут выставить нельзя!")
                return

            if seconds >= 61:
                messagebox.showerror("Ошибка", "Больше 60 секунд выставить нельзя!")
                return

            self.timer_remaining = minutes * 60 + seconds
            if self.timer_remaining <= 0:
                messagebox.showwarning("Ошибка", "Укажите время больше нуля")
                return

        self.timer_running = True
        self.set_status("Таймер запущен")
        self.tick_timer()

    def tick_timer(self):
        if not self.timer_running:
            return

        minutes, seconds = divmod(self.timer_remaining, 60)
        self.timer_display.config(text=f"{minutes:02d}:{seconds:02d}")

        if self.timer_remaining <= 0:
            self.timer_running = False
            self.set_status("Время вышло")
            messagebox.showinfo("Таймер", "Время вышло!")
            return

        self.timer_remaining -= 1
        self.timer_job = self.root.after(1000, self.tick_timer)

    def pause_timer(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_running = False
        self.set_status("Таймер на паузе")

    def reset_timer(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_running = False
        self.timer_remaining = 0
        self.timer_display.config(text="00:00")
        self.set_status("Таймер сброшен")

    # -------------------- ЗАМЕТКИ --------------------

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

    # -------------------- КОНВЕРТОР --------------------

    def create_conv_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Конвертор")

        ttk.Button(frame, text="Шпаргалка", command=lambda: messagebox.showinfo("Шпаргалка", "USD-Доллар,EUR-Евро,RUB-Рубль,KZT-Тенге,UAH-Гривна,GBP-Фунт стерлингов,CNY-Юань,TRY-Турецкая лира,GEL-Лари,BYN-Белорусский_рубль,KGS-Сом,UZS-Сум,CHF-Франк,JPY-Иена")).pack(anchor="ne", padx=10, pady=5)

        ttk.Label(frame, text="Сумма:").pack(pady=(15, 0))
        self.conv_amount_var = tk.StringVar(value="1")
        ttk.Entry(frame, textvariable=self.conv_amount_var, justify="center").pack(pady=5)

        ttk.Label(frame, text="Из валюты:").pack(pady=(10, 0))
        self.conv_var = tk.StringVar(value="KZT")
        self.conv_combo = ttk.Combobox(frame, textvariable=self.conv_var,
                                       values=list(self.CURRENCY_CODES.keys()),
                                       state="readonly", justify="center", width=12)
        self.conv_combo.pack(pady=5)

        ttk.Label(frame, text="В валюту:").pack(pady=(10, 0))
        self.conv1_var = tk.StringVar(value="RUB")
        self.conv1_combo = ttk.Combobox(frame, textvariable=self.conv1_var,
                                        values=list(self.CURRENCY_CODES.keys()),
                                        state="readonly", justify="center", width=12)
        self.conv1_combo.pack(pady=5)

        ttk.Button(frame, text="Конвертировать", command=self.convert_currency).pack(pady=15)

        self.conv_result = ttk.Label(frame, text="Результат:", font=("", 11, "bold"))
        self.conv_result.pack(pady=5)

    def get_live_rate(self, from_cur, to_cur):
        cache_key = f"{from_cur}_{to_cur}"
        now = datetime.now()

        if cache_key in self.rate_cache:
            rate, timestamp = self.rate_cache[cache_key]
            if (now - timestamp).seconds < 3600:
                return rate

        url = f"https://open.er-api.com/v6/latest/{from_cur}"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("result") != "success" or to_cur not in data.get("rates", {}):
            raise Exception("Сервер не вернул курс")

        rate = data["rates"][to_cur]
        self.rate_cache[cache_key] = (rate, now)
        return rate

    def convert_currency(self):
        raw_amount = self.conv_amount_var.get().replace(",", ".").strip()
        try:
            amount = float(raw_amount)
        except ValueError:
            messagebox.showwarning("Ошибка", "Введите корректную сумму (например: 100 или 99.5)")
            return

        if amount >= 9999999:
            messagebox.showerror("Ошибка", "Больше 9999998 Нельзя!")
            return

        if amount <= 0:
            messagebox.showerror("Ошибка", "Менее 0 нельзя!")
            return

        from_cur = self.conv_var.get()
        to_cur = self.conv1_var.get()

        if from_cur == to_cur:
            self.conv_result.config(text=f"Результат: {amount:.2f} {to_cur}")
            messagebox.showinfo("Результат", f"Результат: {amount:.2f} {to_cur}")
            return

        try:
            rate = self.get_live_rate(from_cur, to_cur)
            result = amount * rate
            self.conv_result.config(text=f"Результат: {result:.2f} {to_cur}")
            self.set_status(f"Конвертация: {amount} {from_cur} → {result:.2f} {to_cur}")
            messagebox.showinfo("Результат", f"Результат: {result:.2f} {to_cur}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить курс: {e}")

    # -------------------- ИНФОРМАЦИЯ --------------------

    def create_info_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Инфо")

        ttk.Label(frame, text="Информация:").pack(pady=10)

        info_text = tk.Text(frame, wrap="word", height=15)
        info_text.insert(
            "1.0",
            "Я dfsaetg и я создал это приложение\n"
            "Данное приложение находится в Альфа-тесте.\n"
            "Создано 15.09.2026.\n"
            "*С использованием ИИ*(как искатель ошибок)\n"
            "___________________________________\n"
            "Версия: " + VERS + "\n"
            "Политики:\n"
            "1. Мы не собираем ваши данные. Все файлы хранятся локально на вашем устройстве!\n"
            "___________________________________\n"
            "Обновления:\n"
            "1.0.15-Обновление Генерации пароля теперь максимальная длина до 100 символов\n"
            "1.0.16-Обновление операций в калькуляторе: добавлен новый выбор операций, "
            "оптимизация функций и кода\n"
            "1.0.17-Обновление Тех поддержки, теперь больше способов поддержки и также "
            "наш проект на github и т.д!\n"
            "1.0.18-Обновление счёта калькулятора, добавлены новые операции (//, **), "
            "добавлена вкладка таймер и к ней новые функции,Также добавлена новая вкладка Конвертер\n"
            "1.0.19-Конвертор валют теперь работает\n"
            "1.0.20-Конвертор переведён на реальный API (open.er-api.com), работает на любом Python\n"
            "1.0.21.4-Добавлена вкладка Расчёт средней стоимости и Также исправление некоторых ошибок и уменьшение названий\n"
            "1.0.22-Переработка кода,добавление пасхалки/выхода/шпоргалки из аккаунта и исправление мелочей\n"
            "1.0.23-Сделан свой баннер в начале запуска,исправление пасхалки,Добавлена дата создания аккаунта в профиль,добавленние истории в калькулятор,переделка показа версии\n"
            "1.0.24-Добавлена вкладка Погода (wttr.in, без API-ключа)"

        )
        info_text.config(state="disabled")
        info_text.pack(pady=10, padx=10, fill="both", expand=True)

    # -------------------- ТЕХ. ПОДДЕРЖКА --------------------

    def create_help_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Тех. Поддержка")

        ttk.Label(frame, text="Тех. Поддержка").pack(pady=5)
        ttk.Label(frame, text="Telegram:").pack(pady=5)

        help_entry = ttk.Entry(frame, justify="center")
        help_entry.insert(0, self.TELEGRAM_TAG_HELP)
        help_entry.config(state="readonly")
        help_entry.pack(pady=5)

        ttk.Label(frame, text="Ссылка на github проекта:").pack(pady=5)

        help_entry = ttk.Entry(frame, justify="center")
        help_entry.insert(0, self.GITHUB)
        help_entry.config(state="readonly")
        help_entry.pack(pady=5)

        ttk.Label(frame, text="TikTok Проекта:").pack(pady=5)

        help_entry = ttk.Entry(frame, justify="center")
        help_entry.insert(0, self.TIKTOK)
        help_entry.config(state="readonly")
        help_entry.pack(pady=5)

        ttk.Label(frame, text="Discord Проекта:").pack(pady=5)

        help_entry = ttk.Entry(frame, justify="center")
        help_entry.insert(0, self.DISCORD)
        help_entry.config(state="readonly")
        help_entry.pack(pady=5)

        ttk.Button(frame, text=".",
                   command=lambda: messagebox.showinfo("Пасхалка", "Молодец ты нашёл пасхалку! скинь скрин этого уведомления в поддержку и тебе дадут приз!")
                   ).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = SolarAppV1_1(root)
    root.mainloop()