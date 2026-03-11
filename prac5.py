
import threading
import json
import os
import time
import copy
from enum import IntEnum
from datetime import datetime

class LogLevel(IntEnum):
    INFO = 1
    WARNING = 2
    ERROR = 3

class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_path="logger_config.json"):
        if hasattr(self, "_initialized"):
            return

        self._initialized = True
        self.log_level = LogLevel.INFO
        self.log_file = "app.log"
        self.max_size = 1024 * 1024
        self.console_output = True
        self._file_lock = threading.Lock()

        self.load_config(config_path)

    def load_config(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                self.log_level = LogLevel[data.get("log_level", "INFO")]
                self.log_file = data.get("log_file", "app.log")
                self.max_size = data.get("max_size", 1024 * 1024)
                self.console_output = data.get("console_output", True)

    def set_log_level(self, level):
        self.log_level = level

    def _rotate(self):
        if os.path.exists(self.log_file):
            if os.path.getsize(self.log_file) >= self.max_size:
                base, ext = os.path.splitext(self.log_file)
                new_name = f"{base}_{int(time.time())}{ext}"
                os.rename(self.log_file, new_name)

    def log(self, message, level):
        if level < self.log_level:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = f"{timestamp} [{level.name}] {message}\n"

        with self._file_lock:
            self._rotate()
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(record)

        if self.console_output:
            print(record.strip())



class LogReader:
    def __init__(self, log_file):
        self.log_file = log_file

    def read(self, level=None):
        if not os.path.exists(self.log_file):
            return []

        result = []

        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if level and f"[{level.name}]" not in line:
                    continue
                result.append(line.strip())

        return result


# ===============================
# BUILDER PATTERN
# ===============================
class ReportStyle:
    def __init__(self, bg_color="white", font_color="black", font_size=12):
        self.bg_color = bg_color
        self.font_color = font_color
        self.font_size = font_size


class Report:
    def __init__(self):
        self.header = ""
        self.footer = ""
        self.sections = []
        self.style = None
        self.format = "text"

    def export(self, filename):
        with open(filename, "w", encoding="utf-8") as f:

            if self.format == "html":

                f.write("<html><body>")
                f.write(f"<h1>{self.header}</h1>")

                for name, content in self.sections:
                    f.write(f"<h2>{name}</h2><p>{content}</p>")

                f.write(f"<footer>{self.footer}</footer>")
                f.write("</body></html>")

            else:

                f.write(self.header + "\n")

                for name, content in self.sections:
                    f.write(name + "\n")
                    f.write(content + "\n")

                f.write(self.footer)


class IReportBuilder:
    def set_header(self, header): pass
    def set_footer(self, footer): pass
    def add_section(self, name, content): pass
    def set_style(self, style): pass
    def get_report(self): pass


class TextReportBuilder(IReportBuilder):

    def __init__(self):
        self.report = Report()
        self.report.format = "text"

    def set_header(self, header):
        self.report.header = header

    def set_footer(self, footer):
        self.report.footer = footer

    def add_section(self, name, content):
        self.report.sections.append((name, content))

    def set_style(self, style):
        self.report.style = style

    def get_report(self):
        return self.report


class HtmlReportBuilder(IReportBuilder):

    def __init__(self):
        self.report = Report()
        self.report.format = "html"

    def set_header(self, header):
        self.report.header = header

    def set_footer(self, footer):
        self.report.footer = footer

    def add_section(self, name, content):
        self.report.sections.append((name, content))

    def set_style(self, style):
        self.report.style = style

    def get_report(self):
        return self.report


class ReportDirector:

    def construct_report(self, builder, style):

        builder.set_header("Main Report")
        builder.set_style(style)

        builder.add_section("Introduction", "Dynamic intro content")
        builder.add_section("Data", "Dynamic data section")

        builder.set_footer("Report Footer")

        return builder.get_report()


# ===============================
# PROTOTYPE PATTERN
# ===============================
class Weapon:

    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    def clone(self):
        return copy.deepcopy(self)


class Armor:

    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

    def clone(self):
        return copy.deepcopy(self)


class Skill:

    def __init__(self, name, power):
        self.name = name
        self.power = power

    def clone(self):
        return copy.deepcopy(self)


class Character:

    def __init__(self, health, strength, agility, intelligence, weapon, armor, skills):

        self.health = health
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.weapon = weapon
        self.armor = armor
        self.skills = skills

    def clone(self):

        return Character(
            self.health,
            self.strength,
            self.agility,
            self.intelligence,
            self.weapon.clone(),
            self.armor.clone(),
            [s.clone() for s in self.skills]
        )


# ===============================
# MULTI THREAD TEST
# ===============================
def threaded_logging(thread_id):
    logger = Logger()
    logger.log(f"Thread {thread_id} info", LogLevel.INFO)
    logger.log(f"Thread {thread_id} warning", LogLevel.WARNING)
    logger.log(f"Thread {thread_id} error", LogLevel.ERROR)


# ===============================
# MAIN PROGRAM
# ===============================
if __name__ == "__main__":

    threads = []

    for i in range(5):
        t = threading.Thread(target=threaded_logging, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n--- ERROR LOGS ---")

    reader = LogReader("app.log")
    errors = reader.read(level=LogLevel.ERROR)

    for e in errors:
        print(e)

    # Builder
    style = ReportStyle("lightgray", "blue", 14)

    director = ReportDirector()

    builder = TextReportBuilder()

    report = director.construct_report(builder, style)

    report.export("report.txt")

    print("\nReport exported to report.txt")

    # Prototype
    weapon = Weapon("Sword", 50)
    armor = Armor("Plate", 40)

    skills = [
        Skill("Fireball", 60),
        Skill("Dash", 20)
    ]

    hero = Character(100, 20, 15, 10, weapon, armor, skills)

    clone_hero = hero.clone()

    clone_hero.weapon.name = "Axe"

    print("\nPrototype test:")
    print("Original weapon:", hero.weapon.name)
    print("Cloned weapon:", clone_hero.weapon.name)