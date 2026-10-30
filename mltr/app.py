from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
import requests
import json
import csv
from io import StringIO
from datetime import datetime, timedelta
import os
import re
import random
import time
import webbrowser

# ===================== КОНФИГУРАЦИЯ =====================
BASE_URL = "https://logs.blackrussia.online"
API_URL = f"{BASE_URL}/gslogs/71/api/list-game-logs/"
SITE_URL = f"{BASE_URL}/gslogs/71/"

DEFAULT_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRN_cqqvycZdseUTbNtUUO5esRpamW4WboXojQXk2PtNW_rc8TG-bxxOL2x6sR7Ao788bXD8HBiTTFq/pub?gid=1753284734&single=true&output=csv"

SESSION_FILE = "session.json"
SETTINGS_FILE = "settings.json"

USER_AGENTS = {
    "Firefox": "Mozilla/5.0 (X11; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0",
    "Chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Yandex": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
}

CATEGORIES = {
    'A_casino': 3, 'A_containers': 30, 'B_works': 4,
    'C_trades': 57, 'C_auction': 37, 'C_interaction': 27,
    'D_property': 16, 'D_vehicle': 17,
    'norm_admin': 41, 'norm_super': 45,
}

TRANSFER_THRESHOLD = 150000
GROUP_MINUTES = 15

# ===================== ТЕМЫ =====================
THEMES = {
    'Темная': {
        'bg': (0.10, 0.10, 0.14, 1),
        'card': (0.16, 0.16, 0.22, 1),
        'text': (0.95, 0.95, 1.0, 1),
        'btn_bg': (0.25, 0.25, 0.35, 1),
        'btn_text': (1, 1, 1, 1),
        'input_bg': (0.20, 0.20, 0.28, 1),
        'input_text': (1, 1, 1, 1),
        'accent': (0.30, 0.60, 0.90, 1),
        'green': (0.20, 0.70, 0.30, 1),
        'red': (0.85, 0.20, 0.20, 1),
        'orange': (0.95, 0.55, 0.10, 1),
    },
    'Светлая': {
        'bg': (0.96, 0.96, 0.98, 1),
        'card': (1.0, 1.0, 1.0, 1),
        'text': (0.08, 0.08, 0.12, 1),
        'btn_bg': (0.82, 0.82, 0.88, 1),
        'btn_text': (0.08, 0.08, 0.12, 1),
        'input_bg': (0.92, 0.92, 0.96, 1),
        'input_text': (0.08, 0.08, 0.12, 1),
        'accent': (0.20, 0.50, 0.80, 1),
        'green': (0.15, 0.65, 0.25, 1),
        'red': (0.80, 0.15, 0.15, 1),
        'orange': (0.90, 0.50, 0.05, 1),
    },
    'Черная': {
        'bg': (0.02, 0.02, 0.02, 1),
        'card': (0.06, 0.06, 0.06, 1),
        'text': (0.95, 0.95, 0.95, 1),
        'btn_bg': (0.12, 0.12, 0.12, 1),
        'btn_text': (1, 1, 1, 1),
        'input_bg': (0.08, 0.08, 0.08, 1),
        'input_text': (1, 1, 1, 1),
        'accent': (0.40, 0.40, 0.40, 1),
        'green': (0.15, 0.60, 0.20, 1),
        'red': (0.75, 0.15, 0.15, 1),
        'orange': (0.85, 0.50, 0.10, 1),
    },
    'Синяя': {
        'bg': (0.04, 0.07, 0.14, 1),
        'card': (0.07, 0.11, 0.20, 1),
        'text': (0.90, 0.95, 1.0, 1),
        'btn_bg': (0.10, 0.18, 0.32, 1),
        'btn_text': (1, 1, 1, 1),
        'input_bg': (0.08, 0.14, 0.26, 1),
        'input_text': (1, 1, 1, 1),
        'accent': (0.30, 0.60, 1.0, 1),
        'green': (0.15, 0.65, 0.30, 1),
        'red': (0.85, 0.20, 0.20, 1),
        'orange': (0.95, 0.55, 0.10, 1),
    },
    'Розовая': {
        'bg': (0.22, 0.08, 0.14, 1),
        'card': (0.28, 0.10, 0.18, 1),
        'text': (1.0, 0.90, 0.95, 1),
        'btn_bg': (0.38, 0.12, 0.24, 1),
        'btn_text': (1, 1, 1, 1),
        'input_bg': (0.32, 0.10, 0.20, 1),
        'input_text': (1, 1, 1, 1),
        'accent': (1.0, 0.30, 0.50, 1),
        'green': (0.20, 0.70, 0.35, 1),
        'red': (1.0, 0.25, 0.25, 1),
        'orange': (1.0, 0.60, 0.20, 1),
    },
    'Фиолетовая': {
        'bg': (0.10, 0.04, 0.18, 1),
        'card': (0.14, 0.07, 0.24, 1),
        'text': (0.95, 0.90, 1.0, 1),
        'btn_bg': (0.18, 0.09, 0.32, 1),
        'btn_text': (1, 1, 1, 1),
        'input_bg': (0.16, 0.08, 0.28, 1),
        'input_text': (1, 1, 1, 1),
        'accent': (0.60, 0.30, 1.0, 1),
        'green': (0.20, 0.70, 0.35, 1),
        'red': (0.85, 0.20, 0.20, 1),
        'orange': (0.95, 0.55, 0.10, 1),
    },
}

TEXT_SIZES = [12, 14, 16, 18, 20, 22, 24]

# ===================== УТИЛИТЫ =====================
def get_theme():
    return THEMES.get(App.get_running_app().settings.get('theme', 'Темная'), THEMES['Темная'])

def parse_flexible_date(date_str):
    if not date_str:
        return None
    date_str = date_str.strip()
    parts = date_str.split(' ', 1)
    date_part = parts[0]
    time_part = parts[1] if len(parts) > 1 else None
    date_part = date_part.replace('/', '-').replace('.', '-')
    formats = ['%d-%m-%y', '%d-%m-%Y']
    date_obj = None
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_part, fmt)
            break
        except ValueError:
            continue
    if not date_obj:
        return None
    if time_part:
        try:
            time_obj = datetime.strptime(time_part, '%H:%M')
            date_obj = date_obj.replace(hour=time_obj.hour, minute=time_obj.minute)
        except ValueError:
            pass
    return date_obj

def parse_appointment_date(date_str):
    if not date_str:
        return None
    date_str = date_str.strip()
    date_str = date_str.replace('/', '-').replace('.', '-')
    for fmt in ['%d-%m-%y', '%d-%m-%Y']:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def group_violations_by_time(logs, minutes=GROUP_MINUTES):
    if not logs:
        return []
    def parse_log_time(log):
        t = log.get('time', '')
        try:
            return datetime.fromisoformat(t.replace('+03:00', ''))
        except:
            return datetime.min
    sorted_logs = sorted(logs, key=parse_log_time)
    groups = []
    current_group = [sorted_logs[0]]
    current_time = parse_log_time(sorted_logs[0])
    for log in sorted_logs[1:]:
        log_time = parse_log_time(log)
        if (log_time - current_time).total_seconds() <= minutes * 60:
            current_group.append(log)
        else:
            groups.append(current_group)
            current_group = [log]
            current_time = log_time
    if current_group:
        groups.append(current_group)
    return [g[0] for g in groups]

def format_log_time(time_str):
    try:
        dt = datetime.fromisoformat(time_str.replace('+03:00', ''))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return time_str

# ===================== НАСТРОЙКИ =====================
class SettingsManager:
    def __init__(self):
        self.data = self.load()
    def load(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'theme': 'Темная',
            'text_size': 16,
            'input_position': 'Сверху',
            'sheet_url': DEFAULT_SHEET_URL,
            'timeout': 30,
        }
    def save(self):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.data, f)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
    def get(self, key, default=None):
        return self.data.get(key, default)
    def set(self, key, value):
        self.data[key] = value
        self.save()

# ===================== LOGIN SCREEN =====================
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=12)
        self.build_ui()
        self.add_widget(self.layout)
    
    def build_ui(self):
        self.layout.clear_widgets()
        theme = get_theme()
        ts = App.get_running_app().settings.get('text_size', 16)
        
        header = BoxLayout(orientation='vertical', size_hint_y=0.18, spacing=8)
        header.add_widget(Label(text='[b]Logs BR[/b]', markup=True, font_size=f'{ts+14}sp', color=theme['text']))
        header.add_widget(Label(text='Авторизация', font_size=f'{ts+2}sp', color=theme['text']))
        self.layout.add_widget(header)
        
        help_btn = Button(text='Инструкция', background_color=theme['btn_bg'], color=theme['btn_text'], size_hint_y=0.08, font_size=f'{ts}sp')
        help_btn.bind(on_press=self.show_help)
        self.layout.add_widget(help_btn)
        
        self.layout.add_widget(Label(text='Твой никнейм:', font_size=f'{ts-2}sp', color=theme['text'], size_hint_y=0.05))
        self.nickname_input = TextInput(hint_text='Например: Mikado_Milletary', multiline=False, font_size=f'{ts}sp', size_hint_y=0.08, background_color=theme['input_bg'], foreground_color=theme['input_text'])
        self.layout.add_widget(self.nickname_input)
        
        self.layout.add_widget(Label(text='Session ID:', font_size=f'{ts-2}sp', color=theme['text'], size_hint_y=0.05))
        self.sessionid_input = TextInput(hint_text='sessionid', multiline=False, font_size=f'{ts}sp', size_hint_y=0.08, background_color=theme['input_bg'], foreground_color=theme['input_text'])
        self.layout.add_widget(self.sessionid_input)
        
        self.layout.add_widget(Label(text='CSRF Token:', font_size=f'{ts-2}sp', color=theme['text'], size_hint_y=0.05))
        self.csrftoken_input = TextInput(hint_text='csrftoken', multiline=False, font_size=f'{ts}sp', size_hint_y=0.08, background_color=theme['input_bg'], foreground_color=theme['input_text'])
        self.layout.add_widget(self.csrftoken_input)
        
        login_btn = Button(text='Войти', background_color=theme['green'], color=(1,1,1,1), size_hint_y=0.1, font_size=f'{ts+2}sp')
        login_btn.bind(on_press=self.do_login)
        self.layout.add_widget(login_btn)
        
        self.status_label = Label(text='', font_size=f'{ts-2}sp', color=theme['red'], size_hint_y=0.08)
        self.layout.add_widget(self.status_label)
    
    def show_help(self, instance):
        help_text = (
            "[b]Как получить куки:[/b]\n\n"
            "1. Нажми 'Открыть сайт' ниже\n"
            "2. Пройди капчу и войди в аккаунт\n"
            "3. На ПК: нажми F12, перейди во вкладку Application -> Cookies\n"
            "4. На телефоне (Kiwi Browser): меню -> Developer Tools -> Application -> Cookies\n"
            "5. Найди и скопируй значения sessionid и csrftoken\n"
            "6. Введи свой никнейм, вставь куки и нажми 'Войти'\n\n"
            "Данные сохранятся и не потребуются при следующем входе."
        )
        scroll = ScrollView()
        label = Label(text=help_text, font_size='14sp', padding=[20, 20, 20, 20], halign='left', valign='top', markup=True)
        label.bind(size=label.setter('text_size'))
        scroll.add_widget(label)
        popup = Popup(title='Инструкция по авторизации', content=scroll, size_hint=(0.9, 0.7), auto_dismiss=True)
        popup.open()
    
    def do_login(self, instance):
        nickname = self.nickname_input.text.strip()
        sessionid = self.sessionid_input.text.strip()
        csrftoken = self.csrftoken_input.text.strip()
        if not sessionid or not csrftoken:
            self.status_label.text = "Заполни Session ID и CSRF Token!"
            return
        app = App.get_running_app()
        app.username = nickname if nickname else "Admin"
        app.session.cookies.set("sessionid", sessionid)
        app.session.cookies.set("csrftoken", csrftoken)
        app.session.headers.update({"User-Agent": USER_AGENTS["Chrome"]})
        app.save_session()
        self.status_label.text = "Вход выполнен!"
        self.status_label.color = (0.3, 1, 0.3, 1)
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'main'), 0.8)
    
    def on_enter(self):
        self.build_ui()
        # Заполняем поля последними данными
        app = App.get_running_app()
        last_data = app.get_last_login_data()
        if last_data:
            self.nickname_input.text = last_data.get('nickname', '')
            self.sessionid_input.text = last_data.get('sessionid', '')
            self.csrftoken_input.text = last_data.get('csrftoken', '')

# ===================== MAIN SCREEN =====================
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.build_ui()
        self.add_widget(self.layout)
    
    def build_ui(self):
        self.layout.clear_widgets()
        theme = get_theme()
        ts = App.get_running_app().settings.get('text_size', 16)
        
        top_layout = BoxLayout(size_hint_y=0.12)
        self.account_label = Label(text='[b]Загрузка...[/b]', markup=True, font_size=f'{ts+2}sp', halign='right', color=theme['text'])
        top_layout.add_widget(self.account_label)
        logout_btn = Button(text='Выйти', background_color=theme['red'], color=(1,1,1,1), size_hint_x=0.3, font_size=f'{ts-2}sp')
        logout_btn.bind(on_press=self.do_logout)
        top_layout.add_widget(logout_btn)
        self.layout.add_widget(top_layout)
        
        center_layout = BoxLayout(orientation='vertical', spacing=20, size_hint_y=0.75)
        center_layout.add_widget(Label(text='[b]Logs BR[/b]', markup=True, font_size=f'{ts+32}sp', color=theme['text']))
        
        events_btn = Button(text='Мероприятия', background_color=theme['green'], color=(1,1,1,1), size_hint_y=0.2, font_size=f'{ts+4}sp')
        events_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'events'))
        center_layout.add_widget(events_btn)
        
        check_btn = Button(text='Проверка', background_color=theme['orange'], color=(1,1,1,1), size_hint_y=0.2, font_size=f'{ts+4}sp')
        check_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'check'))
        center_layout.add_widget(check_btn)
        
        norm_btn = Button(text='Норма', background_color=theme['accent'], color=(1,1,1,1), size_hint_y=0.2, font_size=f'{ts+4}sp')
        norm_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'norm'))
        center_layout.add_widget(norm_btn)
        self.layout.add_widget(center_layout)
        
        bottom_layout = BoxLayout(size_hint_y=0.13)
        settings_btn = Button(text='Настройки', background_color=theme['btn_bg'], color=theme['btn_text'], font_size=f'{ts}sp')
        settings_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'settings'))
        bottom_layout.add_widget(settings_btn)
        version_label = Label(text='v0.0.3', font_size=f'{ts-4}sp', color=(0.5, 0.5, 0.6, 1))
        bottom_layout.add_widget(version_label)
        self.layout.add_widget(bottom_layout)
    
    def on_enter(self):
        self.build_ui()
        app = App.get_running_app()
        self.account_label.text = f'[b]{app.username}[/b]'
    
    def do_logout(self, instance):
        app = App.get_running_app()
        app.session.cookies.clear()
        # НЕ удаляем session.json - сохраняем данные для быстрого входа
        self.manager.current = 'login'

# ===================== EVENTS SCREEN =====================
class EventsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cached_results = None
        self.cached_date = None
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        self.build_ui()
        self.add_widget(self.layout)
    
    def build_ui(self):
        self.layout.clear_widgets()
        theme = get_theme()
        ts = App.get_running_app().settings.get('text_size', 16)
        input_pos = App.get_running_app().settings.get('input_position', 'Сверху')
        
        self.layout.add_widget(Label(text='[b]Мероприятия[/b]', markup=True, font_size=f'{ts+10}sp', color=theme['text'], size_hint_y=0.08))
        
        self.results_scroll = ScrollView(size_hint_y=0.70)
        self.results_layout = GridLayout(cols=1, size_hint_y=None, spacing=0)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        
        header = BoxLayout(size_hint_y=None, height=40)
        header.add_widget(Label(text='[b]Ник[/b]', markup=True, font_size=f'{ts}sp', halign='left', valign='middle', color=theme['text'], size_hint_x=0.7))
        header.add_widget(Label(text='[b]Кол-во[/b]', markup=True, font_size=f'{ts}sp', halign='center', valign='middle', color=theme['text'], size_hint_x=0.3))
        self.results_layout.add_widget(header)
        self.results_layout.add_widget(Label(text='─' * 60, font_size=f'{ts-6}sp', color=(0.4, 0.4, 0.5, 1), size_hint_y=None, height=10))
        
        self.results_scroll.add_widget(self.results_layout)
        
        self.progress = ProgressBar(max=100, value=0, size_hint_y=0.04)
        self.progress.opacity = 0
        self.status_label = Label(text='', font_size=f'{ts-4}sp', color=theme['text'], size_hint_y=0.03)
        
        settings_layout = BoxLayout(orientation='vertical', spacing=8, size_hint_y=0.15)
        settings_layout.add_widget(Label(text='Дата (ДД.ММ.ГГГГ):', font_size=f'{ts-2}sp', color=theme['text'], size_hint_y=0.3))
        self.date_input = TextInput(hint_text='28.10.2026', multiline=False, font_size=f'{ts+2}sp', size_hint_y=0.4, background_color=theme['input_bg'], foreground_color=theme['input_text'])
        settings_layout.add_widget(self.date_input)
        
        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.3)
        check_btn = Button(text='Проверить', background_color=theme['green'], color=(1,1,1,1), font_size=f'{ts}sp')
        check_btn.bind(on_press=self.start_check)
        buttons_layout.add_widget(check_btn)
        reset_btn = Button(text='Сбросить', background_color=theme['red'], color=(1,1,1,1), font_size=f'{ts}sp')
        reset_btn.bind(on_press=self.reset_results)
        buttons_layout.add_widget(reset_btn)
        back_btn = Button(text='Назад', background_color=theme['btn_bg'], color=theme['btn_text'], font_size=f'{ts}sp')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        buttons_layout.add_widget(back_btn)
        settings_layout.add_widget(buttons_layout)
        
        if input_pos == 'Сверху':
            self.layout.add_widget(settings_layout)
            self.layout.add_widget(self.results_scroll)
            self.layout.add_widget(self.progress)
            self.layout.add_widget(self.status_label)
        else:
            self.layout.add_widget(self.results_scroll)
            self.layout.add_widget(self.progress)
            self.layout.add_widget(self.status_label)
            self.layout.add_widget(settings_layout)
    
    def on_enter(self):
        self.build_ui()
        if self.cached_results:
            self.restore_results()
    
    def restore_results(self):
        self.date_input.text = self.cached_date or ''
        while len(self.results_layout.children) > 2:
            self.results_layout.remove_widget(self.results_layout.children[-1])
        
        theme = get_theme()
        ts = App.get_running_app().settings.get('text_size', 16)
        
        for nick, count in self.cached_results:
            row_layout = BoxLayout(size_hint_y=None, height=38)
            row_layout.add_widget(Label(text=nick, font_size=f'{ts}sp', halign='left', valign='middle', color=theme['text'], size_hint_x=0.7))
            row_layout.add_widget(Label(text=str(count), font_size=f'{ts}sp', halign='center', valign='middle', color=theme['text'], size_hint_x=0.3))
            self.results_layout.add_widget(row_layout)
            self.results_layout.add_widget(Label(text='─' * 60, font_size=f'{ts-6}sp', color=(0.3, 0.3, 0.4, 1), size_hint_y=None, height=8))
        
        self.status_label.text = f"Восстановлено: {len(self.cached_results)} записей"
    
    def reset_results(self, instance):
        self.cached_results = None
        self.cached_date = None
        while len(self.results_layout.children) > 2:
            self.results_layout.remove_widget(self.results_layout.children[-1])
        self.date_input.text = ''
        self.status_label.text = "Результаты сброшены"
    
    def start_check(self, instance):
        date_str = self.date_input.text.strip()
        check_date = parse_flexible_date(date_str) if date_str else datetime.now().replace(hour=0, minute=0)
        if not check_date:
            self.status_label.text = "Неверный формат даты!"
            return
        while len(self.results_layout.children) > 2:
            self.results_layout.remove_widget(self.results_layout.children[-1])
        self.progress.opacity = 1
        self.progress.value = 0
        self.status_label.text = "Загрузка списка..."
        app = App.get_running_app()
        Clock.schedule_once(lambda dt: self.run_check(app, check_date, date_str), 0.1)
    
    def run_check(self, app, check_date, date_str):
        nicknames = app.load_nicknames()
        if not nicknames:
            self.status_label.text = "Ошибка загрузки списка!"
            self.progress.opacity = 0
            return
        filtered = [row for row in nicknames if not (len(row) > 1 and row[1].strip() == '1 lvl')]
        self.cached_results = []
        self.cached_date = date_str
        total = len(filtered)
        if total == 0:
            self.status_label.text = "Нет админов для проверки!"
            self.progress.opacity = 0
            return
        
        theme = get_theme()
        ts = App.get_running_app().settings.get('text_size', 16)
        
        for i, row in enumerate(filtered, 1):
            nick = row[0]
            count = app.get_event_count(nick, check_date)
            self.cached_results.append((nick, count))
            
            row_layout = BoxLayout(size_hint_y=None, height=38)
            row_layout.add_widget(Label(text=nick, font_size=f'{ts}sp', halign='left', valign='middle', color=theme['text'], size_hint_x=0.7))
            row_layout.add_widget(Label(text=str(count), font_size=f'{ts}sp', halign='center', valign='middle', color=theme['text'], size_hint_x=0.3))
            self.results_layout.add_widget(row_layout)
            self.results_layout.add_widget(Label(text='─' * 60, font_size=f'{ts-6}sp', color=(0.3, 0.3, 0.4, 1), size_hint_y=None, height=8))
            
            self.progress.value = (i / total) * 100
            self.status_label.text = f"Проверено: {i}/{total}"
        
        self.progress.opacity = 0
        self.status_label.text = f"Готово! Проверено {total}."
    


# ===================== CHECK SCREEN =====================
class CheckScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cached_results = None
        self.cached_params = None
        self.admin_checkboxes = {}
        self.all_admins_list = []
        self.all_admins_data = []
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        self.build_ui()
        self.add_widget(self.layout)
    
    def build_ui(self):
        self.layout.clear_widgets()
        theme = get_theme()
        ts = App.get_running_app().settings.get('text_size', 16)
        input_pos = App.get_running_app().settings.get('input_position', 'Сверху')
        
        self.layout.add_widget(Label(text='[b]Проверка администраторов[/b]', markup=True, font_size=f'{ts+8}sp', color=theme['text'], size_hint_y=0.06))
        
        self.admins_btn = Button(text='Выбрать администраторов', background_color=theme['btn_bg'], color=theme['btn_text'], size_hint_y=0.08, font_size=f'{ts}sp')
        self.admins_btn.bind(on_press=self.open_admins_popup)
        
        dates_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.20)
        dates_left = BoxLayout(orientation='vertical', spacing=5)
        dates_left.add_widget(Label(text='С:', font_size=f'{ts-2}sp', color=theme['text']))
        self.date_from = TextInput(hint_text='28.10.2026', multiline=False, font_size=f'{ts}sp', background_color=theme['input_bg'], foreground_color=theme['input_text'])
        dates_left.add_widget(self.date_from)
        dates_layout.add_widget(dates_left)
        dates_right = BoxLayout(orientation='vertical', spacing=5)
        dates_right.add_widget(Label(text='До:', font_size=f'{ts-2}sp', color=theme['text']))
        self.date_to = TextInput(hint_text='28.10.2026', multiline=False, font_size=f'{ts}sp', background_color=theme['input_bg'], foreground_color=theme['input_text'])
        dates_right.add_widget(self.date_to)
        dates_layout.add_widget(dates_right)
        
        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.08)
        check_btn = Button(text='Проверить', background_color=theme['green'], color=(1,1,1,1), font_size=f'{ts}sp')
        check_btn.bind(on_press=self.start_check)
        buttons_layout.add_widget(check_btn)
        reset_btn = Button(text='Сбросить', background_color=theme['red'], color=(1,1,1,1), font_size=f'{ts}sp')
        reset_btn.bind(on_press=self.reset_results)
        buttons_layout.add_widget(reset_btn)
        back_btn = Button(text='Назад', background_color=theme['btn_bg'], color=theme['btn_text'], font_size=f'{ts}sp')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        buttons_layout.add_widget(back_btn)
        
        self.progress = ProgressBar(max=100, value=0, size_hint_y=0.05)
        self.progress.opacity = 0
        self.status_label = Label(text='', font_size=f'{ts-2}sp', color=theme['text'], size_hint_y=0.05)
        self.results_scroll = ScrollView(size_hint_y=0.50)
        self.results_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        self.results_scroll.add_widget(self.results_layout)
        
        if input_pos == 'Сверху':
            self.layout.add_widget(self.admins_btn)
            self.layout.add_widget(dates_layout)
            self.layout.add_widget(buttons_layout)
            self.layout.add_widget(self.progress)
            self.layout.add_widget(self.status_label)
            self.layout.add_widget(self.results_scroll)
        else:
            self.layout.add_widget(self.admins_btn)
            self.layout.add_widget(self.results_scroll)
            self.layout.add_widget(self.progress)
            self.layout.add_widget(self.status_label)
            self.layout.add_widget(dates_layout)
            self.layout.add_widget(buttons_layout)
    
    def on_enter(self):
        self.build_ui()
        if not self.all_admins_data:
            self.status_label.text = "Загрузка списка админов..."
            Clock.schedule_once(lambda dt: self.load_admins(), 0.1)
        if self.cached_results:
            self.restore_results()
    
    def load_admins(self):
        app = App.get_running_app()
        self.all_admins_data = app.load_nicknames()
        # ВАЖНО: сохраняем ВСЕХ админов (включая 1 lvl) для корректной фильтрации трейдов
        self.all_admins_list = [row[0] for row in self.all_admins_data]
        self.admin_checkboxes = {row[0]: False for row in self.all_admins_data}
        self.update_admins_button()
        self.status_label.text = f"Загружено {len(self.all_admins_data)} админов"
    
    def open_admins_popup(self, instance):
        if not self.all_admins_data:
            self.status_label.text = "Сначала дождись загрузки списка"
            return
        theme = get_theme()
        ts = App.get_running_app().settings.get('text_size', 16)
        
        content = BoxLayout(orientation='vertical', spacing=10)
        all_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=45)
        all_checkbox = CheckBox(active=False, size_hint_x=0.1)
        all_label = Label(text='[b]Все[/b]', markup=True, font_size=f'{ts}sp', color=theme['text'])
        all_row.add_widget(all_checkbox)
        all_row.add_widget(all_label)
        content.add_widget(all_row)
        
        scroll = ScrollView(size_hint_y=1)
        grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))
        checkboxes = {}
        for row in self.all_admins_data:
            nick = row[0]
            lvl = row[1] if len(row) > 1 else ''
            row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            cb = CheckBox(active=self.admin_checkboxes.get(nick, False), size_hint_x=0.1)
            cb.bind(active=lambda inst, val, n=nick: self.on_checkbox_change(n, val))
            label = Label(text=f'{nick} ({lvl})', font_size=f'{ts-2}sp', color=theme['text'])
            row_layout.add_widget(cb)
            row_layout.add_widget(label)
            grid.add_widget(row_layout)
            checkboxes[nick] = cb
        scroll.add_widget(grid)
        content.add_widget(scroll)
        
        def toggle_all(cb, active):
            for nick, cb_item in checkboxes.items():
                cb_item.active = active
                self.admin_checkboxes[nick] = active
            self.update_admins_button()
        all_checkbox.bind(active=toggle_all)
        
        popup = Popup(title='Выбор администраторов', content=content, size_hint=(0.9, 0.8))
        close_btn = Button(text='Закрыть', background_color=theme['btn_bg'], color=theme['btn_text'], size_hint_y=None, height=50, font_size=f'{ts}sp')
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        popup.open()
    
    def on_checkbox_change(self, nick, active):
        self.admin_checkboxes[nick] = active
        self.update_admins_button()
    
    def update_admins_button(self):
        selected = sum(1 for v in self.admin_checkboxes.values() if v)
        total = len(self.admin_checkboxes)
        if selected == 0:
            self.admins_btn.text = 'Выбрать администраторов'
        elif selected == total:
            self.admins_btn.text = 'Все'
        else:
            self.admins_btn.text = f'Выбрано {selected}'
    
    def get_selected_admins(self):
        return [nick for nick, active in self.admin_checkboxes.items() if active]
    
    def reset_results(self, instance):
        self.cached_results = None
        self.cached_params = None
        self.results_layout.clear_widgets()
        self.date_from.text = ''
        self.date_to.text = ''
        self.status_label.text = "Результаты сброшены"
    
    def restore_results(self):
        if self.cached_params:
            self.date_from.text = self.cached_params.get('date_from', '')
            self.date_to.text = self.cached_params.get('date_to', '')
        if self.cached_results:
            for admin, blocks in self.cached_results:
                self.display_results(admin, blocks)
            self.status_label.text = f"Восстановлено: {len(self.cached_results)} админов"
    
    def start_check(self, instance):
        # Блокируем проверку до загрузки списка
        if not self.all_admins_data:
            self.status_label.text = "Сначала дождись загрузки списка админов!"
            return
        
        selected = self.get_selected_admins()
        if not selected:
            self.status_label.text = "Выбери хотя бы одного админа!"
            return
        # ... остальной код без изменений
        date_from = parse_flexible_date(self.date_from.text.strip())
        date_to = parse_flexible_date(self.date_to.text.strip())
        if not date_from or not date_to:
            self.status_label.text = "Неверный формат даты!"
            return
        if date_to < date_from:
            self.status_label.text = "Дата 'До' раньше 'С'!"
            return
        self.results_layout.clear_widgets()
        self.progress.opacity = 1
        self.progress.value = 0
        self.cached_params = {'date_from': self.date_from.text, 'date_to': self.date_to.text}
        self.cached_results = []
        Clock.schedule_once(lambda dt: self.run_check(selected, date_from, date_to), 0.1)
    
    def run_check(self, admins, date_from, date_to):
        app = App.get_running_app()
        total = len(admins)
        for i, admin in enumerate(admins, 1):
            self.status_label.text = f"Проверяю {admin} ({i}/{total})..."
            appointment_date = None
            for row in self.all_admins_data:
                if len(row) >= 3 and row[0] == admin:
                    appointment_date = parse_appointment_date(row[2])
                    break
            effective_from = date_from
            if appointment_date and appointment_date > date_from:
                effective_from = appointment_date
            if effective_from > date_to:
                results = {'A': [], 'B': [], 'C_trades': [], 'C_auction': [], 'C_transfers': {}, 'D_property': [], 'D_vehicle': []}
            else:
                results = self.check_admin(app, admin, effective_from, date_to)
            self.cached_results.append((admin, results))
            self.display_results(admin, results)
            self.progress.value = (i / total) * 100
            if i < total:
                time.sleep(random.uniform(4, 10))
        self.progress.opacity = 0
        self.status_label.text = f"Проверка завершена! ({total} адм.)"
    
    def check_admin(self, app, admin, date_from, date_to):
        results = {'A': [], 'B': [], 'C_trades': [], 'C_auction': [], 'C_transfers': {}, 'D_property': [], 'D_vehicle': []}
        for day in self.get_days_range(date_from, date_to):
            day_start = day.replace(hour=8, minute=0, second=0)
            day_end = day.replace(hour=20, minute=0, second=0)
            results['A'].extend(app.get_logs(CATEGORIES['A_casino'], admin, day_start, day_end))
            results['A'].extend(app.get_logs(CATEGORIES['A_containers'], admin, day_start, day_end))
        results['B'] = app.get_logs(CATEGORIES['B_works'], admin, date_from, date_to)
        results['C_trades'] = self.filter_successful_trades(app.get_logs(CATEGORIES['C_trades'], admin, date_from, date_to))
        results['C_auction'] = app.get_logs(CATEGORIES['C_auction'], admin, date_from, date_to)
        results['C_transfers'] = self.analyze_transfers(app.get_logs(CATEGORIES['C_interaction'], admin, date_from, date_to))
        results['D_property'] = self.filter_acquisitions(app.get_logs(CATEGORIES['D_property'], admin, date_from, date_to), ['Приобрел', 'Купил'])
        results['D_vehicle'] = self.filter_acquisitions(app.get_logs(CATEGORIES['D_vehicle'], admin, date_from, date_to), ['Покупка транспорта', 'Приобрел'])
        return results
    
    def get_days_range(self, date_from, date_to):
        days = []
        current = date_from.replace(hour=0, minute=0, second=0)
        end = date_to.replace(hour=0, minute=0, second=0)
        while current <= end:
            days.append(current)
            current += timedelta(days=1)
        return days
    
    def filter_successful_trades(self, logs):
        trades = []
        trade_groups = {}
        for log in logs:
            match = re.search(r'\[TradeID:\s*(\d+)\]', log.get('transaction_desc', ''))
            if match:
                trade_groups.setdefault(match.group(1), []).append(log)
        for trade_id, group in trade_groups.items():
            if any('Обмен успешно закончен' in log.get('transaction_desc', '') for log in group):
                participants = set(log.get('player_name') for log in group)
                # Если ВСЕ участники есть в ПОЛНОМ списке админов — пропускаем (админ-админ)
                if all(p in self.all_admins_list for p in participants):
                    continue
                first_log = group[0]
                trades.append({'trade_id': trade_id, 'time': first_log.get('time', ''), 'participants': ', '.join(participants)})
        return trades
    
    def analyze_transfers(self, logs):
        transfers = {}
        for log in logs:
            desc = log.get('transaction_desc', '')
            amount = log.get('transaction_amount', 0)
            match = re.search(r'(Передача денег игроку|Получение денег от)\s+(\w+)', desc)
            if match:
                other_player = match.group(2)
                transfers[other_player] = transfers.get(other_player, 0) + abs(amount)
        return {p: t for p, t in transfers.items() if t > TRANSFER_THRESHOLD}
    
    def filter_acquisitions(self, logs, keywords):
        return [log for log in logs if any(kw in log.get('transaction_desc', '') for kw in keywords) and not log.get('transaction_desc', '').startswith('+')]
    
    def display_results(self, admin, results):
        theme = get_theme()
        ts = App.get_running_app().settings.get('text_size', 16)
        
        admin_block = BoxLayout(orientation='vertical', size_hint_y=None, padding=8, spacing=4)
        admin_block.bind(minimum_height=admin_block.setter('height'))
        
        header = Label(text=f'[b]{admin}[/b]', markup=True, font_size=f'{ts+2}sp', color=theme['accent'], size_hint_y=None, height=30, halign='left')
        header.bind(size=header.setter('text_size'))
        admin_block.add_widget(header)
        
        # Блок A — БЕЗ \n после "чисто"
        a_grouped = group_violations_by_time(results['A'])
        a_text = f'[b]Блок A (08:00-20:00):[/b] '
        if not a_grouped:
            a_text += '[color=00ff00]чисто[/color]'  # Нет \n
        else:
            a_text += f'[color=ff0000]{len(a_grouped)} нар.[/color]\n'
            for log in a_grouped:
                a_text += f'  {format_log_time(log.get("time", ""))}\n'
        a_label = Label(text=a_text, markup=True, font_size=f'{ts-2}sp', color=theme['text'], size_hint_y=None, halign='left', valign='top')
        a_label.bind(size=a_label.setter('text_size'))
        admin_block.add_widget(a_label)
        
        # Блок B — БЕЗ \n после "чисто"
        b_grouped = group_violations_by_time(results['B'])
        b_text = f'[b]Блок B (Работы):[/b] '
        if not b_grouped:
            b_text += '[color=00ff00]чисто[/color]'  # Нет \n
        else:
            b_text += f'[color=ff0000]{len(b_grouped)} нар.[/color]\n'
            for log in b_grouped:
                b_text += f'  {format_log_time(log.get("time", ""))}\n'
        b_label = Label(text=b_text, markup=True, font_size=f'{ts-2}sp', color=theme['text'], size_hint_y=None, halign='left', valign='top')
        b_label.bind(size=b_label.setter('text_size'))
        admin_block.add_widget(b_label)
        
        # Блок C — БЕЗ \n после "чисто"
        c_text = f'[b]Блок C:[/b] '
        has_c = False
        if results['C_trades']:
            has_c = True
            c_text += f'\n  Трейды: {len(results["C_trades"])}\n'
            for t in results['C_trades']:
                c_text += f'    ID:{t["trade_id"]} {format_log_time(t["time"])}\n'
        if results['C_auction']:
            has_c = True
            c_text += f'  Аукцион: {len(results["C_auction"])} зап.\n'
        if results['C_transfers']:
            has_c = True
            c_text += f'  Переводы >150k:\n'
            for p, t in results['C_transfers'].items():
                c_text += f'    {p}: {t:,}р.\n'
        if not has_c:
            c_text += '[color=00ff00]чисто[/color]'  # Нет \n
        c_label = Label(text=c_text, markup=True, font_size=f'{ts-2}sp', color=theme['text'], size_hint_y=None, halign='left', valign='top')
        c_label.bind(size=c_label.setter('text_size'))
        admin_block.add_widget(c_label)
        
        # Блок D — БЕЗ \n после "чисто"
        d_text = f'[b]Блок D:[/b] '
        has_d = False
        if results['D_property']:
            has_d = True
            d_text += f'\n  Имущество: {len(results["D_property"])}\n'
            for log in results['D_property']:
                d_text += f'    {format_log_time(log.get("time", ""))}\n'
        if results['D_vehicle']:
            has_d = True
            d_text += f'  Транспорт: {len(results["D_vehicle"])}\n'
            for log in results['D_vehicle']:
                d_text += f'    {format_log_time(log.get("time", ""))}\n'
        if not has_d:
            d_text += '[color=00ff00]чисто[/color]'  # Нет \n
        d_label = Label(text=d_text, markup=True, font_size=f'{ts-2}sp', color=theme['text'], size_hint_y=None, halign='left', valign='top')
        d_label.bind(size=d_label.setter('text_size'))
        admin_block.add_widget(d_label)
        
        separator = Label(text='─' * 40, font_size=f'{ts-4}sp', color=(0.3, 0.3, 0.4, 1), size_hint_y=None, height=15)
        admin_block.add_widget(separator)
        
        self.results_layout.add_widget(admin_block)

# ===================== NORM SCREEN =====================
class NormScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.build_ui()
        self.add_widget(self.layout)
    
    def build_ui(self):
        self.layout.clear_widgets()
        theme = get_theme()
        ts = App.get_running_app().settings.get('text_size', 16)
        input_pos = App.get_running_app().settings.get('input_position', 'Сверху')
        
        self.layout.add_widget(Label(text='[b]Норма[/b]', markup=True, font_size=f'{ts+10}sp', color=theme['text'], size_hint_y=0.1))
        self.result_label = Label(text='', font_size=f'{ts+8}sp', color=theme['text'], size_hint_y=0.3)
        back_btn = Button(text='Назад', background_color=theme['btn_bg'], color=theme['btn_text'], size_hint_y=0.1, font_size=f'{ts}sp')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        
        input_layout = BoxLayout(orientation='vertical', spacing=8, size_hint_y=0.15)
        input_layout.add_widget(Label(text='Дата (необязательно, по умолчанию сегодня):', font_size=f'{ts-2}sp', color=theme['text'], size_hint_y=0.3))
        self.date_input = TextInput(hint_text='28.10.2026', multiline=False, font_size=f'{ts+2}sp', size_hint_y=0.4, background_color=theme['input_bg'], foreground_color=theme['input_text'])
        input_layout.add_widget(self.date_input)
        check_btn = Button(text='Посчитать', background_color=theme['accent'], color=(1,1,1,1), size_hint_y=0.3, font_size=f'{ts}sp')
        check_btn.bind(on_press=self.start_check)
        input_layout.add_widget(check_btn)
        
        if input_pos == 'Сверху':
            self.layout.add_widget(input_layout)
            self.layout.add_widget(self.result_label)
            self.layout.add_widget(back_btn)
        else:
            self.layout.add_widget(self.result_label)
            self.layout.add_widget(input_layout)
            self.layout.add_widget(back_btn)
    
    def on_enter(self):
        self.build_ui()
    
    def start_check(self, instance):
        date_str = self.date_input.text.strip()
        check_date = parse_flexible_date(date_str) if date_str else datetime.now().replace(hour=0, minute=0)
        if not check_date:
            self.result_label.text = "Неверный формат даты!"
            return
        app = App.get_running_app()
        username = app.username
        date_from = check_date.replace(hour=0, minute=0, second=0)
        date_to = check_date.replace(hour=23, minute=59, second=59)
        count_admin = len(app.get_logs(CATEGORIES['norm_admin'], username, date_from, date_to))
        count_super = len(app.get_logs(CATEGORIES['norm_super'], username, date_from, date_to))
        total = count_admin + count_super
        self.result_label.text = f'Норма за {check_date.strftime("%d.%m.%Y")}:\n\n{total} записей'

# ===================== SETTINGS SCREEN =====================
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.build_ui()
        self.add_widget(self.layout)
    
    def build_ui(self):
        self.layout.clear_widgets()
        theme = get_theme()
        ts = App.get_running_app().settings.get('text_size', 16)
        
        self.layout.add_widget(Label(text='[b]Настройки[/b]', markup=True, font_size=f'{ts+10}sp', color=theme['text'], size_hint_y=0.1))
        
        content = BoxLayout(orientation='vertical', spacing=15, size_hint_y=0.75)
        
        content.add_widget(Label(text='Тема:', font_size=f'{ts}sp', color=theme['text'], size_hint_y=0.1))
        self.theme_spinner = Spinner(text=App.get_running_app().settings.get('theme', 'Темная'), values=list(THEMES.keys()), size_hint_y=0.15, background_color=theme['input_bg'], color=theme['input_text'])
        self.theme_spinner.bind(text=self.on_theme_change)
        content.add_widget(self.theme_spinner)
        
        content.add_widget(Label(text='Размер текста:', font_size=f'{ts}sp', color=theme['text'], size_hint_y=0.1))
        self.size_spinner = Spinner(text=str(App.get_running_app().settings.get('text_size', 16)), values=[str(s) for s in TEXT_SIZES], size_hint_y=0.15, background_color=theme['input_bg'], color=theme['input_text'])
        self.size_spinner.bind(text=self.on_size_change)
        content.add_widget(self.size_spinner)
        
        content.add_widget(Label(text='Расположение полей ввода:', font_size=f'{ts}sp', color=theme['text'], size_hint_y=0.1))
        self.pos_spinner = Spinner(text=App.get_running_app().settings.get('input_position', 'Сверху'), values=['Сверху', 'Снизу'], size_hint_y=0.15, background_color=theme['input_bg'], color=theme['input_text'])
        self.pos_spinner.bind(text=self.on_pos_change)
        content.add_widget(self.pos_spinner)
        
        dev_btn = Button(text='Настройки разработчика', background_color=theme['accent'], color=(1,1,1,1), size_hint_y=0.15, font_size=f'{ts}sp')
        dev_btn.bind(on_press=self.open_dev_settings)
        content.add_widget(dev_btn)
        
        self.layout.add_widget(content)
        back_btn = Button(text='Назад', background_color=theme['btn_bg'], color=theme['btn_text'], size_hint_y=0.1, font_size=f'{ts}sp')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        self.layout.add_widget(back_btn)
    
    def on_enter(self):
        self.build_ui()
    
    def on_theme_change(self, spinner, text):
        App.get_running_app().settings.set('theme', text)
        App.get_running_app().apply_theme()
    
    def on_size_change(self, spinner, text):
        App.get_running_app().settings.set('text_size', int(text))
    
    def on_pos_change(self, spinner, text):
        App.get_running_app().settings.set('input_position', text)
    
    def open_dev_settings(self, instance):
        theme = get_theme()
        ts = App.get_running_app().settings.get('text_size', 16)
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text='Пароль:', font_size=f'{ts}sp', size_hint_y=0.15))
        password_input = TextInput(hint_text='Введите пароль', password=True, multiline=False, font_size=f'{ts}sp', size_hint_y=0.2, background_color=theme['input_bg'], foreground_color=theme['input_text'])
        content.add_widget(password_input)
        unlock_btn = Button(text='Разблокировать', background_color=theme['accent'], color=(1,1,1,1), size_hint_y=0.2, font_size=f'{ts}sp')
        content.add_widget(unlock_btn)
        popup = Popup(title='Настройки разработчика', content=content, size_hint=(0.9, 0.5))
        def try_unlock(btn):
            if password_input.text == 'password':
                popup.dismiss()
                self.show_dev_panel()
            else:
                password_input.hint_text = 'Неверный пароль!'
        unlock_btn.bind(on_press=try_unlock)
        popup.open()
    
    def show_dev_panel(self):
        app = App.get_running_app()
        theme = get_theme()
        ts = App.get_running_app().settings.get('text_size', 16)
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text='Ссылка на таблицу:', font_size=f'{ts-2}sp', size_hint_y=0.15))
        sheet_input = TextInput(text=app.settings.get('sheet_url', DEFAULT_SHEET_URL), multiline=False, font_size=f'{ts-2}sp', size_hint_y=0.25, background_color=theme['input_bg'], foreground_color=theme['input_text'])
        content.add_widget(sheet_input)
        content.add_widget(Label(text='Таймаут запросов (сек):', font_size=f'{ts-2}sp', size_hint_y=0.15))
        timeout_input = TextInput(text=str(app.settings.get('timeout', 30)), multiline=False, font_size=f'{ts}sp', size_hint_y=0.2, background_color=theme['input_bg'], foreground_color=theme['input_text'])
        content.add_widget(timeout_input)
        save_btn = Button(text='Сохранить', background_color=theme['green'], color=(1,1,1,1), size_hint_y=0.2, font_size=f'{ts}sp')
        content.add_widget(save_btn)
        popup = Popup(title='Настройки разработчика', content=content, size_hint=(0.9, 0.6))
        def save(btn):
            app.settings.set('sheet_url', sheet_input.text.strip())
            try:
                app.settings.set('timeout', int(timeout_input.text.strip()))
            except:
                pass
            popup.dismiss()
        save_btn.bind(on_press=save)
        popup.open()

# ===================== APP =====================
class BlackLogApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = requests.Session()
        self.username = "Admin"
        self.settings = SettingsManager()
        self.load_session()
    
    def build(self):
        self.apply_theme()
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(EventsScreen(name='events'))
        sm.add_widget(CheckScreen(name='check'))
        sm.add_widget(NormScreen(name='norm'))
        sm.add_widget(SettingsScreen(name='settings'))
        if self.session.cookies.get("sessionid"):
            sm.current = 'main'
        return sm
    
    def apply_theme(self):
        theme_name = self.settings.get('theme', 'Темная')
        theme = THEMES.get(theme_name, THEMES['Темная'])
        Window.clearcolor = theme['bg']
    
    def load_session(self):
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r") as f:
                    data = json.load(f)
                    self.session.cookies.update(data.get("cookies", {}))
                    self.username = data.get("username", "Admin")
                    self.session.headers.update({"User-Agent": USER_AGENTS["Chrome"]})
            except:
                pass
    
    def save_session(self):
        try:
            with open(SESSION_FILE, "w") as f:
                json.dump({
                    "cookies": dict(self.session.cookies),
                    "username": self.username,
                    "last_login": {
                        "nickname": self.username,
                        "sessionid": self.session.cookies.get("sessionid", ""),
                        "csrftoken": self.session.cookies.get("csrftoken", ""),
                    }
                }, f)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def get_last_login_data(self):
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("last_login", {})
            except:
                pass
        return {}
    
    def load_nicknames(self):
        timeout = self.settings.get('timeout', 30)
        sheet_url = self.settings.get('sheet_url', DEFAULT_SHEET_URL)
        try:
            response = requests.get(sheet_url, timeout=timeout)
            response.raise_for_status()
            reader = csv.reader(StringIO(response.text))
            result = []
            for row in reader:
                if len(row) >= 2 and row[0].strip():
                    nick = row[0].strip()
                    lvl = row[1].strip()
                    date_appt = row[2].strip() if len(row) >= 3 else ''
                    result.append((nick, lvl, date_appt))
            return result
        except Exception as e:
            print(f"Ошибка Google Sheets: {e}")
            if os.path.exists("admins.txt"):
                with open("admins.txt", "r", encoding="utf-8") as f:
                    return [tuple(line.strip().split(',')) + ('',) for line in f if ',' in line]
            return [("Viktor_Pronenko", "4 lvl", ""), ("Mikado_Milletary", "5 lvl", "")]
    
    def get_event_count(self, nickname, date):
        timeout = self.settings.get('timeout', 30)
        params = {"offset": 0, "limit": 200, "order_by": "time", "auto": "false",
                  "category_id__exact": 41, "player_name__exact": nickname,
                  "time__gte": date.strftime("%Y-%m-%dT00:00"), "time__lte": (date + timedelta(days=1)).strftime("%Y-%m-%dT00:00"),
                  "transaction_desc__ilike": "%создал мероприятие%"}
        try:
            response = self.session.get(API_URL, params=params, timeout=timeout)
            if response.status_code == 429:
                time.sleep(5)
                response = self.session.get(API_URL, params=params, timeout=timeout)
            response.raise_for_status()
            return len(response.json())
        except:
            return 0
    
    def get_logs(self, category_id, player_name, date_from, date_to):
        timeout = self.settings.get('timeout', 30)
        params = {"offset": 0, "limit": 200, "order_by": "time", "auto": "false",
                  "category_id__exact": category_id, "player_name__exact": player_name,
                  "time__gte": date_from.strftime("%Y-%m-%dT%H:%M"), "time__lte": date_to.strftime("%Y-%m-%dT%H:%M")}
        try:
            response = self.session.get(API_URL, params=params, timeout=timeout)
            if response.status_code == 429:
                time.sleep(5)
                response = self.session.get(API_URL, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except:
            return []

if __name__ == '__main__':
    BlackLogApp().run()