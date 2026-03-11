import threading
import json
import copy


# ==================================
# SINGLETON PATTERN
# ==================================

class ConfigurationManager:

    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if hasattr(self, "_initialized"):
            return

        self.settings = {}
        self._initialized = True

    @classmethod
    def get_instance(cls):

        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = ConfigurationManager()

        return cls._instance

    def load_from_file(self, filename):

        try:
            with open(filename, "r") as f:
                self.settings = json.load(f)

        except FileNotFoundError:
            print("Config file not found")

    def save_to_file(self, filename):

        with open(filename, "w") as f:
            json.dump(self.settings, f)

    def set(self, key, value):
        self.settings[key] = value

    def get(self, key):

        if key not in self.settings:
            raise Exception("Setting not found")

        return self.settings[key]


# ==================================
# BUILDER PATTERN
# ==================================

class Report:

    def __init__(self):
        self.header = ""
        self.content = ""
        self.footer = ""

    def show(self):
        print(self.header)
        print(self.content)
        print(self.footer)


class IReportBuilder:

    def set_header(self, header): pass
    def set_content(self, content): pass
    def set_footer(self, footer): pass
    def get_report(self): pass


class TextReportBuilder(IReportBuilder):

    def __init__(self):
        self.report = Report()

    def set_header(self, header):
        self.report.header = header

    def set_content(self, content):
        self.report.content = content

    def set_footer(self, footer):
        self.report.footer = footer

    def get_report(self):
        return self.report


class HtmlReportBuilder(IReportBuilder):

    def __init__(self):
        self.report = Report()

    def set_header(self, header):
        self.report.header = f"<h1>{header}</h1>"

    def set_content(self, content):
        self.report.content = f"<p>{content}</p>"

    def set_footer(self, footer):
        self.report.footer = f"<footer>{footer}</footer>"

    def get_report(self):
        return self.report


class ReportDirector:

    def construct(self, builder):

        builder.set_header("Sales Report")
        builder.set_content("Report content here...")
        builder.set_footer("2026")

        return builder.get_report()


# ==================================
# PROTOTYPE PATTERN
# ==================================

class Product:

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def clone(self):
        return copy.deepcopy(self)


class Discount:

    def __init__(self, name, percent):
        self.name = name
        self.percent = percent

    def clone(self):
        return copy.deepcopy(self)


class Order:

    def __init__(self, products, delivery_cost, discounts, payment_method):

        self.products = products
        self.delivery_cost = delivery_cost
        self.discounts = discounts
        self.payment_method = payment_method

    def clone(self):

        return Order(
            [p.clone() for p in self.products],
            self.delivery_cost,
            [d.clone() for d in self.discounts],
            self.payment_method
        )

    def show(self):

        print("Payment:", self.payment_method)

        for p in self.products:
            print(p.name, p.price, p.quantity)

        print("Delivery:", self.delivery_cost)

        for d in self.discounts:
            print("Discount:", d.name, d.percent)


# ==================================
# TEST PROGRAM
# ==================================

def singleton_test():

    def worker():
        config = ConfigurationManager.get_instance()
        print("Instance id:", id(config))

    threads = []

    for _ in range(5):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":

    print("===== SINGLETON TEST =====")

    config = ConfigurationManager.get_instance()
    config.set("theme", "dark")
    config.set("language", "ru")

    print(config.get("theme"))

    singleton_test()

    print("\n===== BUILDER TEST =====")

    director = ReportDirector()

    text_builder = TextReportBuilder()
    report1 = director.construct(text_builder)
    report1.show()

    html_builder = HtmlReportBuilder()
    report2 = director.construct(html_builder)
    report2.show()

    print("\n===== PROTOTYPE TEST =====")

    p1 = Product("Laptop", 1000, 1)
    p2 = Product("Mouse", 50, 2)

    d1 = Discount("Black Friday", 10)

    order1 = Order([p1, p2], 20, [d1], "Card")

    order2 = order1.clone()

    order2.products[0].name = "Gaming Laptop"

    print("\nOriginal order:")
    order1.show()

    print("\nCloned order:")
    order2.show()
