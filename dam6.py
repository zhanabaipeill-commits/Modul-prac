from abc import ABC, abstractmethod


# ======================================
# STRATEGY PATTERN (Payment System)
# ======================================

class PaymentStrategy(ABC):

    @abstractmethod
    def pay(self, amount):
        pass


class CreditCardPayment(PaymentStrategy):

    def pay(self, amount):
        print(f"Paid {amount} using Credit Card")


class PayPalPayment(PaymentStrategy):

    def pay(self, amount):
        print(f"Paid {amount} using PayPal")


class CryptoPayment(PaymentStrategy):

    def pay(self, amount):
        print(f"Paid {amount} using Cryptocurrency")


class PaymentContext:

    def __init__(self):
        self.strategy = None

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_payment(self, amount):

        if not self.strategy:
            print("Payment strategy not selected")
            return

        self.strategy.pay(amount)


# ======================================
# OBSERVER PATTERN (Currency Exchange)
# ======================================

class Observer(ABC):

    @abstractmethod
    def update(self, currency, rate):
        pass


class Subject(ABC):

    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self, currency, rate):
        pass


class CurrencyExchange(Subject):

    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, currency, rate):

        for observer in self.observers:
            observer.update(currency, rate)

    def set_rate(self, currency, rate):

        print(f"\nCurrency {currency} updated to {rate}")

        self.notify(currency, rate)


# ======================================
# OBSERVERS
# ======================================

class Trader(Observer):

    def update(self, currency, rate):
        print(f"Trader received update: {currency} = {rate}")


class MobileApp(Observer):

    def update(self, currency, rate):
        print(f"Mobile app notification: {currency} = {rate}")


class AnalyticsSystem(Observer):

    def update(self, currency, rate):
        print(f"Analytics system processed rate: {currency} = {rate}")


# ======================================
# MAIN PROGRAM
# ======================================

if __name__ == "__main__":

    print("=== STRATEGY PATTERN (Payment System) ===")

    context = PaymentContext()

    print("Choose payment method:")
    print("1 - Credit Card")
    print("2 - PayPal")
    print("3 - Cryptocurrency")

    choice = int(input("Enter choice: "))

    if choice == 1:
        context.set_strategy(CreditCardPayment())

    elif choice == 2:
        context.set_strategy(PayPalPayment())

    elif choice == 3:
        context.set_strategy(CryptoPayment())

    else:
        print("Invalid choice")

    context.execute_payment(100)

    print("\n=== OBSERVER PATTERN (Currency Exchange) ===")

    exchange = CurrencyExchange()

    trader = Trader()
    mobile = MobileApp()
    analytics = AnalyticsSystem()

    exchange.attach(trader)
    exchange.attach(mobile)
    exchange.attach(analytics)

    exchange.set_rate("USD", 470)
    exchange.set_rate("EUR", 510)

    exchange.detach(mobile)

    exchange.set_rate("BTC", 60000)
