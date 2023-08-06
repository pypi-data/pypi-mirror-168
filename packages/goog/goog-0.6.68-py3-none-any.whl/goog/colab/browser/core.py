from omnitools import abs_dir
from ..utils import runShell
import os


def start(sc_port):
    t = open(os.path.join(abs_dir(__file__), "webkit_browser.py"), "rb").read().decode()
    t = t.replace("'<sc_port>'", str(sc_port))
    open("webkit_browser.py", "wb").write(t.encode())
    runShell("python3.7 webkit_browser.py")


def startWebkit(sc_port):
    return start(sc_port)


