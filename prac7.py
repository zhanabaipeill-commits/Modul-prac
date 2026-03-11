
import time
from abc import ABC, abstractmethod


class ICommand(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...


class Light:
    def __init__(self, n):
        self.n = n
        self.on = False

    def on_(self):
        self.on = True
        print("Light", self.n, "ON")

    def off_(self):
        self.on = False
        print("Light", self.n, "OFF")


class TV:
    def __init__(self, n):
        self.n = n
        self.on = False

    def on_(self):
        self.on = True
        print("TV", self.n, "ON")

    def off_(self):
        self.on = False
        print("TV", self.n, "OFF")


class AC:
    def __init__(self, n):
        self.n = n
        self.on = False
        self.t = 24

    def on_(self):
        self.on = True
        print("AC", self.n, "ON", self.t)

    def off_(self):
        self.on = False
        print("AC", self.n, "OFF")

    def set_(self, t):
        self.t = t
        self.on = True
        print("AC", self.n, "SET", self.t)


class Cmd(ICommand):
    def __init__(self, do, un):
        self.do = do
        self.un = un

    def execute(self):
        self.do()

    def undo(self):
        self.un()


class Macro(ICommand):
    def __init__(self, cmds):
        self.cmds = cmds

    def execute(self):
        for c in self.cmds:
            c.execute()

    def undo(self):
        for c in self.cmds[::-1]:
            c.undo()


class Remote:
    def __init__(self, k=6):
        self.on = [None] * k
        self.off = [None] * k
        self.u = []
        self.r = []
        self.rec = False
        self.buf = []

    def set(self, i, on, off):
        self.on[i] = on
        self.off[i] = off

    def _run(self, c):
        if not c:
            print("Empty")
            return
        c.execute()
        self.u.append(c)
        self.r.clear()
        if self.rec:
            self.buf.append(c)

    def press_on(self, i):
        self._run(self.on[i])

    def press_off(self, i):
        self._run(self.off[i])

    def undo(self):
        if not self.u:
            print("Undo empty")
            return
        c = self.u.pop()
        c.undo()
        self.r.append(c)

    def redo(self):
        if not self.r:
            print("Redo empty")
            return
        c = self.r.pop()
        c.execute()
        self.u.append(c)

    def rec_start(self):
        self.rec = True
        self.buf = []
        print("REC START")

    def rec_stop(self):
        self.rec = False
        print("REC STOP")
        return Macro(self.buf[:])


class ReportGenerator(ABC):
    def generate(self, data):
        self.validate(data)
        title = self.title()
        body = self.body(data)
        rep = self.compose(title, body)

        if self.want():
            self.deliver(rep)

        return rep

    def validate(self, data):
        if data is None:
            raise ValueError("data")

    def title(self):
        return f"Report({self.kind()})"

    @abstractmethod
    def kind(self): ...

    @abstractmethod
    def body(self, data): ...

    def compose(self, t, b):
        return t + "\n" + b

    def want(self):
        a = input(f"Deliver {self.kind()}? (y/n): ").strip().lower()
        if a not in {"y", "n"}:
            raise ValueError("y/n")
        return a == "y"

    def deliver(self, rep):
        print("DELIVER", self.kind(), "\n" + rep)


class PdfReport(ReportGenerator):
    def kind(self):
        return "PDF"

    def body(self, data):
        return " | ".join(",".join(f"{k}={v}" for k, v in d.items()) for d in data)


class ExcelReport(ReportGenerator):
    def __init__(self, path="report.tsv"):
        self.path = path

    def kind(self):
        return "Excel"

    def body(self, data):
        keys = sorted({k for d in data for k in d})
        rows = ["\t".join(keys)]
        rows += ["\t".join(str(d.get(k, "")) for k in keys) for d in data]
        return "\n".join(rows)

    def deliver(self, rep):
        open(self.path, "w", encoding="utf-8").write(rep + "\n")
        print("SAVED", self.path)


class HtmlReport(ReportGenerator):
    def kind(self):
        return "HTML"

    def body(self, data):
        keys = sorted({k for d in data for k in d})

        th = "".join(f"<th>{k}</th>" for k in keys)

        trs = "".join(
            "<tr>" + "".join(f"<td>{d.get(k,'')}</td>" for k in keys) + "</tr>"
            for d in data
        )

        return f"<table border=1><tr>{th}</tr>{trs}</table>"

    def compose(self, t, b):
        return f"<h1>{t}</h1>{b}<p>{time.strftime('%Y-%m-%d %H:%M:%S')}</p>"


class IMediator(ABC):
    @abstractmethod
    def join(self, u, ch): ...

    @abstractmethod
    def send(self, u, ch, msg): ...

    @abstractmethod
    def pm(self, u, to, msg): ...


class Mediator(IMediator):
    def __init__(self):
        self.ch = {}
        self.users = {}

    def join(self, u, ch):
        self.ch.setdefault(ch, set()).add(u.n)
        self.users[u.n] = u

        for name in self.ch[ch]:
            if name != u.n:
                self.users[name].sys(ch, f"{u.n} joined")

        u.sys(ch, "Joined")

    def send(self, u, ch, msg):
        if ch not in self.ch:
            print("No channel")
            return

        if u.n not in self.ch[ch]:
            u.sys(ch, "Not in channel")
            return

        for name in self.ch[ch]:
            if name != u.n:
                self.users[name].recv(ch, u.n, msg)

    def pm(self, u, to, msg):
        if to not in self.users:
            print("No user")
            return

        self.users[to].recv("PM", u.n, msg)


class User:
    def __init__(self, n, m):
        self.n = n
        self.m = m

    def recv(self, ch, fr, msg):
        print(f"[{ch}] {fr}->{self.n}: {msg}")

    def sys(self, ch, msg):
        print(f"[{ch}] *{self.n}: {msg}")

    def join(self, ch):
        self.m.join(self, ch)

    def send(self, ch, msg):
        self.m.send(self, ch, msg)

    def pm(self, to, msg):
        self.m.pm(self, to, msg)


if __name__ == "__main__":

    l = Light("Hall")
    tv = TV("LG")
    ac = AC("Gree")

    r = Remote(4)

    r.set(0, Cmd(l.on_, l.off_), Cmd(l.off_, l.on_))
    r.set(1, Cmd(tv.on_, tv.off_), Cmd(tv.off_, tv.on_))
    r.set(2, Cmd(lambda: ac.set_(20), lambda: ac.set_(24)), Cmd(ac.off_, ac.on_))

    r.press_on(0)
    r.press_on(1)
    r.undo()
    r.redo()

    mc = Macro([
        Cmd(l.on_, l.off_),
        Cmd(tv.on_, tv.off_),
        Cmd(lambda: ac.set_(18), lambda: ac.set_(24))
    ])

    r.set(3, mc, Macro([
        Cmd(l.off_, l.on_),
        Cmd(tv.off_, tv.on_),
        Cmd(ac.off_, ac.on_)
    ]))

    r.press_on(3)
    r.undo()

    r.rec_start()
    r.press_on(0)
    r.press_on(2)
    rec = r.rec_stop()

    rec.execute()
    rec.undo()

    data = [{"name": "A", "score": 10}, {"name": "B", "score": 20}]

    PdfReport().generate(data)
    ExcelReport("report.tsv").generate(data)
    HtmlReport().generate(data)

    m = Mediator()

    a = User("Ali", m)
    b = User("Bota", m)
    c = User("Daulet", m)

    a.join("general")
    b.join("general")
    c.join("dev")

    a.send("general", "Salem")
    b.pm("Ali", "Privet")
    c.send("general", "hi")