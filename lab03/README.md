# Лабораторная работа 3 Посетитель (Visitor)

### Проблема
В системе «Умный дом» при добавлении новых комплексных сценариев (например, «Ночной режим», «Режим вечеринки» или «Отпуск») логика управления устройствами начинает распределяться по самим классам устройств (Light, Thermostat, SmartLock). 
Это приводит к двум проблемам:
1. Чтобы добавить новый сценарий, приходится изменять код каждого класса устройства.
2. Засорение классов, устройства начинают содержать логику, которая не относится к их прямой ответственности (хранению состояния и базовому управлению).

### Классы:
* **SmartHome (Client / ObjectStructure):** Управляющий класс, хранящий коллекцию устройств и запускающий выполнение сценариев.
* **interface Visitor:** Описывает общий интерфейс для всех сценариев, объявляя методы посещения для каждого типа устройств: visitLight(), visitThermostat(), visitLock().
* **ConcreteVisitors (NightModeVisitor, PartyModeVisitor):** Реализуют конкретную логику поведения устройств для каждого режима.
* **interface SmartDevice (Element):** Базовый интерфейс устройства с методом accept(v: Visitor), который позволяет «впустить» сценарий.
* **ConcreteElements (Light, Thermostat, SmartLock):** Классы устройств, хранящие свои уникальные состояния (поля).

---

### Методы

* **accept(v: Visitor)**: Реализован в каждом устройстве. Цель метода — вызвать у посетителя v функцию, соответствующую типу устройства:
    * В классе Light: v.visitLight(this)
    * В классе Thermostat: v.visitThermostat(this)
    * В классе SmartLock: v.visitLock(this)
 
<img width="1184" height="592" alt="1 лаба-классы лаб 2-3" src="https://github.com/user-attachments/assets/142109ec-a206-468a-aaa9-97866fa990fb" />


### 1. Интерфейсы
- Visitor: Абстрактный интерфейс посетителя. Объявляет методы `visitLight`, `visitThermostat` и `visitLock` для взаимодействия с каждым типом оборудования.
- Element: Абстрактный интерфейс элемента системы. Содержит метод `accept(v: Visitor)`, реализующий механизм двойной диспетчеризации.

### 2. Устройства ConcreteElements
Классы устройств хранят состояние и атрибуты в формате `camelCase` согласно UML:
- Light: Поля `status`, `brightness`, `color`.
- Thermostat: Поля `currentTemp`, `targetTemp`, `mode`.
- SmartLock: Поля `isLocked`, `lastAccessed`, `batteryLevel`.

### 3. Сценарии ConcreteVisitors
Классы, инкапсулирующие логику управления устройствами:
- NightModeVisitor: Устанавливает экономичный режим.
- PartyModeVisitor: Включает праздничный режим.

### 4. Клиентская часть
SmartHome: Класс «структуры объектов».
addDevice(d: Element) — добавление устройства в систему.
applyScenario(v: Visitor) — применение выбранного сценария ко всем устройствам через цикл.

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

* **visitLight(l: Light) / visitThermostat(t: Thermostat)**: Методы внутри Посетителя, которые содержат бизнес-логику сценария. Например, NightModeVisitor через эти методы выключает свет и переводит термостат в эконом-режим.

* **applyScenario(v: Visitor)**: Метод в классе SmartHome, который в цикле обходит все устройства в списке devices и вызывает у каждого метод accept(v).

### Вывод:

Паттерн посетитель позволяет избежать изменений в каждом классе оборудования, теперь новые сценарии внедряются простым созданием нового класса-посетителя. Классы устройств были перегружены. Они отвечали и за хранение своего состояния (яркость, температура), и за алгоритмы поведения в разных сценариях. Паттерн позволяет выстроить четкую иерархию, но его использование не оправдано, если иерархия элементов будет часто меняться в дальнейшем
