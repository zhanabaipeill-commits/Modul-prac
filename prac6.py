import threading
import time
import random
from abc import ABC, abstractmethod


# ===============================
# STRATEGY PATTERN
# ===============================

class ICostCalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, distance, passengers, service_class, extras):
        pass


class FlightCostStrategy(ICostCalculationStrategy):
    def calculate(self, distance, passengers, service_class, extras):
        base_rate = 0.5
        cost = distance * base_rate

        if service_class == "business":
            cost *= 1.8

        if extras.get("baggage", 0) > 0:
            cost += 30 * extras["baggage"]

        cost *= passengers
        return cost


class TrainCostStrategy(ICostCalculationStrategy):
    def calculate(self, distance, passengers, service_class, extras):
        base_rate = 0.2
        cost = distance * base_rate

        if service_class == "business":
            cost *= 1.4

        cost *= passengers
        return cost


class BusCostStrategy(ICostCalculationStrategy):
    def calculate(self, distance, passengers, service_class, extras):
        base_rate = 0.1
        cost = distance * base_rate
        cost *= passengers
        return cost


class TravelBookingContext:

    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy):
        self._strategy = strategy

    def calculate_cost(self, distance, passengers, service_class, extras, discount):

        if not self._strategy:
            raise Exception("Strategy not selected")

        total = self._strategy.calculate(distance, passengers, service_class, extras)

        total *= (1 - discount)

        return total


# ===============================
# OBSERVER PATTERN
# ===============================

class IObserver(ABC):

    @abstractmethod
    def update(self, stock, price):
        pass


class ISubject(ABC):

    @abstractmethod
    def attach(self, observer, stock):
        pass

    @abstractmethod
    def detach(self, observer, stock):
        pass

    @abstractmethod
    def notify(self, stock, price):
        pass


class StockExchange(ISubject):

    def __init__(self):
        self._observers = {}
        self._prices = {}
        self._log = []

    def attach(self, observer, stock):

        self._observers.setdefault(stock, []).append(observer)

        self._log.append(f"{observer.name} subscribed to {stock}")

    def detach(self, observer, stock):

        if stock in self._observers and observer in self._observers[stock]:
            self._observers[stock].remove(observer)

            self._log.append(f"{observer.name} unsubscribed from {stock}")

    def set_price(self, stock, price):

        self._prices[stock] = price

        self._log.append(f"{stock} price changed to {price}")

        self.notify(stock, price)

    def notify(self, stock, price):

        if stock in self._observers:

            for observer in self._observers[stock]:
                threading.Thread(target=observer.update, args=(stock, price)).start()

    def report(self):

        return "\n".join(self._log)


class Trader(IObserver):

    def __init__(self, name):
        self.name = name
        self.notifications = 0

    def update(self, stock, price):

        self.notifications += 1

        print(f"Trader {self.name} notified: {stock} = {price}")


class TradingRobot(IObserver):

    def __init__(self, name, threshold):

        self.name = name
        self.threshold = threshold

    def update(self, stock, price):

        if price < self.threshold:
            print(f"Robot {self.name} buys {stock} at {price}")

        else:
            print(f"Robot {self.name} sells {stock} at {price}")


# ===============================
# MAIN PROGRAM
# ===============================

if __name__ == "__main__":

    print("=== Travel Booking System ===")

    context = TravelBookingContext()

    transport = input("Transport (flight/train/bus): ").lower()
    distance = float(input("Distance: "))
    passengers = int(input("Passengers: "))
    service_class = input("Class (economy/business): ").lower()
    baggage = int(input("Baggage count: "))
    discount_type = input("Discount (none/child/pensioner): ").lower()

    discount = 0

    if discount_type == "child":
        discount = 0.2

    elif discount_type == "pensioner":
        discount = 0.15

    extras = {"baggage": baggage}

    if transport == "flight":
        context.set_strategy(FlightCostStrategy())

    elif transport == "train":
        context.set_strategy(TrainCostStrategy())

    elif transport == "bus":
        context.set_strategy(BusCostStrategy())

    else:
        print("Invalid transport")
        exit()

    try:
        total_cost = context.calculate_cost(distance, passengers, service_class, extras, discount)

        print(f"Total cost: {total_cost}")

    except Exception as e:
        print(e)

    print("\n=== Stock Exchange System ===")

    exchange = StockExchange()

    trader1 = Trader("Ali")

    robot1 = TradingRobot("Robo1", 100)

    exchange.attach(trader1, "AAPL")
    exchange.attach(robot1, "AAPL")
    exchange.attach(trader1, "GOOG")

    stocks = ["AAPL", "GOOG"]

    for _ in range(5):

        stock = random.choice(stocks)

        price = random.randint(80, 150)

        exchange.set_price(stock, price)

        time.sleep(1)

    print("\n=== Log Report ===")

    print(exchange.report())