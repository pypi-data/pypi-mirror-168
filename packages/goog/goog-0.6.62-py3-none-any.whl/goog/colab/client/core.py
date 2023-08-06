from omnitools import abs_dir
from ..utils import runShell
from .utils import rpc
import os


def start(sc_port):
    from ..cell import webkit_GUI_hook
    t = open(os.path.join(abs_dir(__file__), "webkit_browser_utils.py"), "rb").read().decode()
    open("webkit_browser_utils.py", "wb").write(t.encode())
    t = open(os.path.join(abs_dir(__file__), "webkit_browser.py"), "rb").read().decode()
    t = t.replace("'<sc_port>'", str(sc_port)).replace("require_session=False", "require_session=True")
    open("webkit_browser.py", "wb").write(t.encode())
    runShell("python3.7 webkit_browser.py")
    RPC = rpc(sc_port)
    webkit_GUI = webkit_GUI_hook(sc_port, _enable_input=False)
    webkit_GUI.rpc = RPC
    return webkit_GUI

