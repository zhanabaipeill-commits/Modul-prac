from abc import ABC, abstractmethod


# =====================================================
# COMMAND PATTERN (Smart Home)
# =====================================================

class Command(ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


# ----------- Receivers (devices) -----------

class Light:

    def on(self):
        print("Light ON")

    def off(self):
        print("Light OFF")


class Door:

    def open(self):
        print("Door OPENED")

    def close(self):
        print("Door CLOSED")


class Thermostat:

    def increase(self):
        print("Temperature increased")

    def decrease(self):
        print("Temperature decreased")


# ----------- Commands -----------

class LightOnCommand(Command):

    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()


class LightOffCommand(Command):

    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.off()

    def undo(self):
        self.light.on()


class DoorOpenCommand(Command):

    def __init__(self, door):
        self.door = door

    def execute(self):
        self.door.open()

    def undo(self):
        self.door.close()


class DoorCloseCommand(Command):

    def __init__(self, door):
        self.door = door

    def execute(self):
        self.door.close()

    def undo(self):
        self.door.open()


class TempUpCommand(Command):

    def __init__(self, thermostat):
        self.thermostat = thermostat

    def execute(self):
        self.thermostat.increase()

    def undo(self):
        self.thermostat.decrease()


class TempDownCommand(Command):

    def __init__(self, thermostat):
        self.thermostat = thermostat

    def execute(self):
        self.thermostat.decrease()

    def undo(self):
        self.thermostat.increase()


# ----------- Invoker -----------

class RemoteControl:

    def __init__(self):
        self.history = []

    def press(self, command):
        command.execute()
        self.history.append(command)

    def undo(self):

        if not self.history:
            print("Nothing to undo")
            return

        command = self.history.pop()
        command.undo()


# =====================================================
# TEMPLATE METHOD PATTERN (Beverages)
# =====================================================

class Beverage(ABC):

    def prepare_recipe(self):

        self.boil_water()
        self.brew()
        self.pour_in_cup()

        if self.customer_wants_condiments():
            self.add_condiments()

    def boil_water(self):
        print("Boiling water")

    def pour_in_cup(self):
        print("Pouring into cup")

    @abstractmethod
    def brew(self):
        pass

    @abstractmethod
    def add_condiments(self):
        pass

    def customer_wants_condiments(self):

        answer = input("Add condiments? (y/n): ").lower()

        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("Invalid input")
            return False


class Tea(Beverage):

    def brew(self):
        print("Steeping the tea")

    def add_condiments(self):
        print("Adding lemon")


class Coffee(Beverage):

    def brew(self):
        print("Dripping coffee through filter")

    def add_condiments(self):
        print("Adding sugar and milk")


class HotChocolate(Beverage):

    def brew(self):
        print("Mixing chocolate powder")

    def add_condiments(self):
        print("Adding marshmallows")


# =====================================================
# MEDIATOR PATTERN (Chat System)
# =====================================================

class Mediator(ABC):

    @abstractmethod
    def send_message(self, message, user):
        pass

    @abstractmethod
    def add_user(self, user):
        pass


class ChatRoom(Mediator):

    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)
        print(f"{user.name} joined chat")

    def send_message(self, message, sender):

        for user in self.users:
            if user != sender:
                user.receive(message, sender.name)


class User:

    def __init__(self, name, chatroom):

        self.name = name
        self.chatroom = chatroom

    def send(self, message):

        print(f"{self.name} sends: {message}")
        self.chatroom.send_message(message, self)

    def receive(self, message, sender):

        print(f"{self.name} received from {sender}: {message}")


# =====================================================
# MAIN (Client code)
# =====================================================

if __name__ == "__main__":

    print("=== COMMAND PATTERN ===")

    light = Light()
    door = Door()
    thermostat = Thermostat()

    remote = RemoteControl()

    remote.press(LightOnCommand(light))
    remote.press(DoorOpenCommand(door))
    remote.press(TempUpCommand(thermostat))

    print("Undo last command")
    remote.undo()

    print("\n=== TEMPLATE METHOD ===")

    tea = Tea()
    tea.prepare_recipe()

    print()

    coffee = Coffee()
    coffee.prepare_recipe()

    print("\n=== MEDIATOR ===")

    chat = ChatRoom()

    user1 = User("Ali", chat)
    user2 = User("Aruzhan", chat)
    user3 = User("Dias", chat)

    chat.add_user(user1)
    chat.add_user(user2)
    chat.add_user(user3)

    user1.send("Hello everyone!")
    user2.send("Hi Ali!")
