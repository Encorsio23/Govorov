import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, Button, Spinbox, Scale, HORIZONTAL
import random
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


# интерфейс Visitor
class Visitor(ABC):
    @abstractmethod
    def visitLight(self, light): pass

    @abstractmethod
    def visitThermostat(self, thermostat): pass

    @abstractmethod
    def visitLock(self, lock): pass


# интерфейс Element
class Element(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def accept(self, visitor: Visitor):
        pass


# Конкретные элементы
class Light(Element):
    def __init__(self, name):
        super().__init__(name)
        self.status = False
        self.brightness = 0
        self.color = "#FFFFFF"

    def accept(self, visitor: Visitor):
        visitor.visitLight(self)


class Thermostat(Element):
    def __init__(self, name):
        super().__init__(name)
        self.current_temp = random.uniform(15.0, 30.0)
        self.target_temp = 22.0

    def get_system_status(self):
        diff = float(self.target_temp) - self.current_temp
        if abs(diff) < 0.5: return "Выключен"
        return "Отопление" if diff > 0 else "Охлаждение"

    def accept(self, visitor: Visitor):
        visitor.visitThermostat(self)


class SmartLock(Element):
    def __init__(self, name):
        super().__init__(name)
        self.is_locked = True
        self.battery_level = random.randint(15, 100)
        self.last_access = (datetime.now() - timedelta(hours=2)).strftime("%H:%M")

    def accept(self, visitor: Visitor):
        visitor.visitLock(self)


# Сценарии (посетители)
class NightModeVisitor(Visitor):
    def visitLight(self, light):
        light.status = False
        light.brightness = 0

    def visitThermostat(self, thermostat):
        thermostat.target_temp = 18.0

    def visitLock(self, lock):
        lock.is_locked = True
        lock.last_access = datetime.now().strftime("%H:%M")


class PartyModeVisitor(Visitor):
    def visitLight(self, light):
        light.status = True
        light.brightness = 100
        light.color = f'#{random.randint(100, 255):02x}{random.randint(100, 255):02x}{random.randint(100, 255):02x}'

    def visitThermostat(self, thermostat):
        thermostat.target_temp = 24.0

    def visitLock(self, lock):
        lock.is_locked = False
        lock.last_access = datetime.now().strftime("%H:%M")


#SmartHome
class SmartHome:
    def __init__(self):
        self.devices = []

    def addDevice(self, device):
        self.devices.append(device)

    def applyScenario(self, visitor: Visitor):
        for device in self.devices:
            device.accept(visitor)


#GUI

class SmartHomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Умный дом")
        self.root.geometry("600x600")

        # Инициализация модели через SmartHome
        self.home = SmartHome()
        self.light = Light("Гостиная")
        self.term = Thermostat("Спальня")
        self.lock = SmartLock("Входная дверь")

        self.home.addDevice(self.light)
        self.home.addDevice(self.term)
        self.home.addDevice(self.lock)

        # Отрисовка интерфейса (как в версии без паттерна)
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

        # Кнопки сценариев
        frame_scenarios = Frame(root, padx=10, pady=10)
        frame_scenarios.pack(fill='x')

        tk.Label(frame_scenarios, text="Управление сценариями:", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        tk.Button(frame_scenarios, text="🌙 Режим: НОЧЬ", width=18, bg="#2c3e50", fg="white",
                  command=lambda: self.run_scenario(NightModeVisitor())).pack(side=tk.RIGHT, padx=5)

        tk.Button(frame_scenarios, text="🎉 Режим: ВЕЧЕРИНКА", width=18, bg="#e67e22", fg="white",
                  command=lambda: self.run_scenario(PartyModeVisitor())).pack(side=tk.RIGHT, padx=5)

        self.update_all_views()

    def _create_light_ui(self):
        f = self.frame_light
        Label(f, text="Устройство: Гостиная", font=("Arial", 11, "bold")).pack(anchor="w")
        self.light_status_lbl = Label(f, text="Статус: --", font=("Arial", 10))
        self.light_status_lbl.pack(pady=(10, 0), anchor="w")
        self.color_indicator = Frame(f, width=50, height=50, bg="black", highlightbackground="grey",
                                     highlightthickness=1)
        self.color_indicator.pack(pady=5, anchor="w")
        self.color_indicator.pack_propagate(False)
        Label(f, text="Регулировка яркости (%):", font=("Arial", 9)).pack(pady=(10, 0), anchor="w")
        self.bright_scale = Scale(f, from_=0, to=100, orient=HORIZONTAL, length=200,
                                  command=self.on_light_brightness_change)
        self.bright_scale.pack(pady=5, anchor="w")
        Button(f, text="ВКЛ/ВЫКЛ", command=self.on_light_toggle).pack(pady=10)

    def _create_thermostat_ui(self):
        f = self.frame_term
        Label(f, text="Устройство: Спальня", font=("Arial", 11, "bold")).pack(anchor="w")
        self.current_temp_lbl = Label(f, text="--°C", font=("Arial", 12))
        self.current_temp_lbl.pack(pady=10, anchor="w")
        self.term_status_lbl = Label(f, text="Статус: --", font=("Arial", 10))
        self.term_status_lbl.pack(anchor="w")
        Label(f, text="Целевая температура:", font=("Arial", 9)).pack(pady=(15, 0), anchor="w")
        self.target_temp_spin = Spinbox(f, from_=15.0, to=30.0, increment=0.5, font=('Arial', 12),
                                        command=self.on_target_temp_change)
        self.target_temp_spin.pack(pady=5, anchor="w")

    def _create_lock_ui(self):
        f = self.frame_lock
        Label(f, text="Устройство: Входная дверь", font=("Arial", 11, "bold")).pack(anchor="w")
        self.lock_status_lbl = Label(f, text="--", font=("Arial", 12, "bold"))
        self.lock_status_lbl.pack(pady=10, anchor="w")
        self.battery_lbl = Label(f, text="Заряд батареи: --%")
        self.battery_lbl.pack(anchor="w")
        self.last_access_lbl = Label(f, text="Последнее событие: --")
        self.last_access_lbl.pack(anchor="w")
        Button(f, text="ОТКРЫТЬ/ЗАКРЫТЬ", command=self.on_lock_toggle).pack(pady=10)

    def run_scenario(self, visitor: Visitor):
        self.home.applyScenario(visitor)
        self.update_all_views()
        messagebox.showinfo("Умный дом", f"Применен сценарий: {visitor.__class__.__name__}")

    def update_all_views(self):
        self.light_status_lbl.config(
            text=f"Статус: {'ВКЛ' if self.light.status else 'ВЫКЛ'} ({self.light.brightness}%)")
        self.color_indicator.config(bg=self.light.color if self.light.status else "black")
        if self.bright_scale.get() != self.light.brightness: self.bright_scale.set(self.light.brightness)
        self.current_temp_lbl.config(text=f"Текущая темп: {self.term.current_temp:.1f}°C")
        self.term_status_lbl.config(text=f"Статус системы: {self.term.get_system_status()}")
        self.target_temp_spin.delete(0, tk.END);
        self.target_temp_spin.insert(0, f"{self.term.target_temp:.1f}")
        status = "ЗАКРЫТ" if self.lock.is_locked else "ОТКРЫТ"
        self.lock_status_lbl.config(text=f"Статус: {status}", fg="red" if self.lock.is_locked else "green")
        self.battery_lbl.config(text=f"Заряд батареи: {self.lock.battery_level}%")
        self.last_access_lbl.config(text=f"Последнее действие: {self.lock.last_access}")

    def on_light_toggle(self):
        self.light.status = not self.light.status
        self.light.brightness = 100 if self.light.status else 0
        self.update_all_views()

    def on_light_brightness_change(self, val):
        self.light.brightness = int(val)
        self.light.status = self.light.brightness > 0
        self.update_all_views()

    def on_target_temp_change(self):
        self.term.target_temp = float(self.target_temp_spin.get())
        self.update_all_views()

    def on_lock_toggle(self):
        self.lock.is_locked = not self.lock.is_locked
        self.lock.last_access = datetime.now().strftime("%H:%M")
        self.update_all_views()


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeApp(root)
    root.mainloop()
