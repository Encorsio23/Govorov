import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, Button, Spinbox, Scale, HORIZONTAL
import random
from datetime import datetime, timedelta


def get_random_color():
    return f'#{random.randint(50, 255):02x}{random.randint(50, 255):02x}{random.randint(50, 255):02x}'


def get_random_time():
    past_minutes = random.randint(1, 120)
    event_time = datetime.now() - timedelta(minutes=past_minutes)
    return event_time.strftime("%H:%M")


class Light:
    def __init__(self, name):
        self.name = name
        self.status = False
        self.brightness = 0
        self.color = "#FFFFFF"  # Белый по умолчанию

    def set_night_mode(self):
        self.status = False
        self.brightness = 0

    def set_party_mode(self):
        # включить на максимум со случайным цветом
        self.status = True
        self.brightness = 100
        self.color = get_random_color()


class Thermostat:
    def __init__(self, name):
        self.name = name
        # Задается случайно
        self.current_temp = random.uniform(15.0, 30.0)
        self.target_temp = 22.0

    def get_system_status(self):
        diff = float(self.target_temp) - self.current_temp
        if abs(diff) < 0.5: return "Выключен"
        if diff > 0: return "Отопление"
        return "Охлаждение"

    def set_night_mode(self):
        self.target_temp = 18.0

    def set_party_mode(self):
        self.target_temp = 23.0


class SmartLock:
    def __init__(self, name):
        self.name = name
        self.is_locked = True
        self.battery_level = random.randint(10, 100)
        self.last_access = get_random_time()

    def update_access_time(self):
        self.last_access = datetime.now().strftime("%H:%M")

    def toggle(self):
        self.is_locked = not self.is_locked
        self.update_access_time()

    def set_night_mode(self):
        if not self.is_locked:
            self.toggle()

    def set_party_mode(self):
        if self.is_locked:
            self.toggle()


# --- GUI ПРИЛОЖЕНИЕ НА TKINTER (БЕЗ ПАТТЕРНА) ---

class SmartHomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Умный дом")
        self.root.geometry("600x600")

        # Настройка стилей (опционально)
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=(10, 5), font=('Arial', 10, 'bold'))

        # Создаем объекты напрямую
        self.light = Light("Гостиная")
        self.term = Thermostat("Спальня")
        self.lock = SmartLock("Входная дверь")

        # Главный контейнер (Tabs/Вкладки)
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # 1. Вкладка ЛАМПА
        self.frame_light = Frame(notebook, bg="#f9f9f9", padx=10, pady=10)
        notebook.add(self.frame_light, text="Лампа")
        self._create_light_ui()

        # 2. Вкладка ТЕРМОСТАТ
        self.frame_term = Frame(notebook, bg="#f9f9f9", padx=10, pady=10)
        notebook.add(self.frame_term, text="Термостат")
        self._create_thermostat_ui()

        # 3. Вкладка ЗАМОК
        self.frame_lock = Frame(notebook, bg="#f9f9f9", padx=10, pady=10)
        notebook.add(self.frame_lock, text="Замок")
        self._create_lock_ui()

        # Контейнер для кнопок сценариев
        frame_scenarios = Frame(root, padx=10, pady=10)
        frame_scenarios.pack(fill='x')

        tk.Label(frame_scenarios, text="Управление сценариями:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        tk.Button(frame_scenarios, text="Режим: НОЧЬ", width=20, bg="#2c3e50", fg="white",
                  command=self.apply_night).pack(side=tk.RIGHT, padx=5)

        tk.Button(frame_scenarios, text="Режим: ВЕЧЕРИНКА", width=20, bg="#e67e22", fg="white",
                  command=self.apply_party).pack(side=tk.RIGHT, padx=5)

        self.update_all_views()

    # --- ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ СОЗДАНИЯ ИНТЕРФЕЙСА ---

    def _create_light_ui(self):
        f = self.frame_light
        Label(f, text="Устройство: Гостиная", font=("Arial", 11, "bold")).pack(anchor="w")

        # Индикатор цвета (просто цветной квадрат)
        self.light_status_lbl = Label(f, text="Статус: ВЫКЛ", font=("Arial", 10))
        self.light_status_lbl.pack(pady=(10, 0), anchor="w")

        # Рамка индикатора цвета
        self.color_indicator = Frame(f, width=50, height=50, bg="black", highlightbackground="grey",
                                     highlightthickness=1)
        self.color_indicator.pack(pady=5, anchor="w")
        self.color_indicator.pack_propagate(False)  # Фикс размера

        # Регулировка яркости (Слайдер)
        Label(f, text="Регулировка яркости (%):", font=("Arial", 9)).pack(pady=(10, 0), anchor="w")
        self.bright_scale = Scale(f, from_=0, to=100, orient=HORIZONTAL, length=200,
                                  command=self.on_light_brightness_change)
        self.bright_scale.pack(pady=5, anchor="w")

        # Кнопка Вкл/Выкл
        self.light_toggle_btn = Button(f, text="ВКЛ/ВЫКЛ", command=self.on_light_toggle)
        self.light_toggle_btn.pack(pady=10)

    def _create_thermostat_ui(self):
        f = self.frame_term
        Label(f, text="Устройство: Спальня", font=("Arial", 11, "bold")).pack(anchor="w")

        # Текущая температура (read-only)
        self.current_temp_lbl = Label(f, text="Текущая темп: --°C", font=("Arial", 12))
        self.current_temp_lbl.pack(pady=10, anchor="w")

        # Статус системы
        self.term_status_lbl = Label(f, text="Статус: --", font=("Arial", 10))
        self.term_status_lbl.pack(anchor="w")

        # Целевая температура (Spinbox - поле ввода со стрелками)
        Label(f, text="Установить целевую температуру:", font=("Arial", 9)).pack(pady=(15, 0), anchor="w")
        self.target_temp_spin = Spinbox(f, from_=15.0, to=30.0, increment=0.5, font=('Arial', 12),
                                        command=self.on_target_temp_change)
        self.target_temp_spin.pack(pady=5, anchor="w")

    def _create_lock_ui(self):
        f = self.frame_lock
        Label(f, text="Устройство: Входная дверь", font=("Arial", 11, "bold")).pack(anchor="w")

        # Статус замка
        self.lock_status_lbl = Label(f, text="Статус: --", font=("Arial", 12, "bold"))
        self.lock_status_lbl.pack(pady=10, anchor="w")

        # Уровень заряда
        self.battery_lbl = Label(f, text="Заряд батареи: --%", font=("Arial", 10))
        self.battery_lbl.pack(anchor="w")

        # Последнее событие
        self.last_access_lbl = Label(f, text="Последнее открытие/закрытие: --:--", font=("Arial", 9))
        self.last_access_lbl.pack(anchor="w")

        # Кнопка открыть/закрыть
        self.lock_toggle_btn = Button(f, text="ОТКРЫТЬ/ЗАКРЫТЬ", command=self.on_lock_toggle)
        self.lock_toggle_btn.pack(pady=10)

    # --- МЕТОДЫ ОБНОВЛЕНИЯ ИНТЕРФЕЙСА (СИНХРОНИЗАЦИЯ С МОДЕЛЬЮ) ---

    def update_all_views(self):
        self.update_light_view()
        self.update_thermostat_view()
        self.update_lock_view()

    def update_light_view(self):
        self.light_status_lbl.config(
            text=f"Статус: {'ВКЛ' if self.light.status else 'ВЫКЛ'} ({self.light.brightness}%)")
        color = self.light.color if self.light.status else "black"
        self.color_indicator.config(bg=color)

        # Обновляем слайдер только если он не совпадает с моделью (избегаем зацикливания событий)
        if self.bright_scale.get() != self.light.brightness:
            self.bright_scale.set(self.light.brightness)

    def update_thermostat_view(self):
        self.current_temp_lbl.config(text=f"Текущая темп: {self.term.current_temp:.1f}°C")
        self.term_status_lbl.config(text=f"Статус: {self.term.get_system_status()}")

        # Синхронизация Spinbox
        val_in_gui = float(self.target_temp_spin.get())
        if val_in_gui != self.term.target_temp:
            self.target_temp_spin.delete(0, tk.END)
            self.target_temp_spin.insert(0, f"{self.term.target_temp:.1f}")

    def update_lock_view(self):
        status = "ЗАКРЫТ" if self.lock.is_locked else "ОТКРЫТ"
        color = "#e74c3c" if self.lock.is_locked else "#2ecc71"  # Красный/Зеленый
        self.lock_status_lbl.config(text=f"Статус: {status}", fg=color)
        self.battery_lbl.config(text=f"Заряд батареи: {self.lock.battery_level}%")
        self.last_access_lbl.config(text=f"Последнее открытие/закрытие: {self.lock.last_access}")

    # --- ОБРАБОТЧИКИ СОБЫТИЙ GUI (ИЗМЕНЕНИЕ СОСТОЯНИЯ ЧЕРЕЗ ИНТЕРФЕЙС) ---

    def on_light_toggle(self):
        self.light.status = not self.light.status
        self.light.brightness = 100 if self.light.status else 0
        if self.light.status and self.light.color == "#FFFFFF":
            self.light.color = get_random_color()
        self.update_light_view()

    def on_light_brightness_change(self, val):
        self.light.brightness = int(val)
        if self.light.brightness > 0:
            self.light.status = True
            if self.light.color == "#FFFFFF":
                self.light.color = get_random_color()
        else:
            self.light.status = False
        self.update_light_view()

    def on_target_temp_change(self):
        try:
            self.term.target_temp = float(self.target_temp_spin.get())
            self.update_thermostat_view()
        except ValueError:
            pass  # Игнорируем неверный ввод

    def on_lock_toggle(self):
        self.lock.toggle()
        self.update_lock_view()

    # --- КНОПКИ СЦЕНАРИЕВ (СЕРДЦЕ ПРОБЛЕМЫ: ЖЕСТКАЯ ЛОГИКА ТУТ) ---

    def apply_night(self):
        # Проблема: вызываем специфичные методы сценариев у каждого типа объекта
        self.light.set_night_mode()
        self.term.set_night_mode()
        self.lock.set_night_mode()
        self.update_all_views()
        messagebox.showinfo("Умный дом", "Активирован сценарий НОЧЬ")

    def apply_party(self):
        # Проблема: то же самое, жесткое дублирование вызовов
        self.light.set_party_mode()
        self.term.set_party_mode()
        self.lock.set_party_mode()
        self.update_all_views()
        messagebox.showinfo("Умный дом", "Время веселиться! (Случайные цвета включены)")


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeApp(root)
    root.mainloop()