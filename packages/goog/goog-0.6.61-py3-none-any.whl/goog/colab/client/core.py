from omnitools import abs_dir
from ..utils import runShell
from .utils import rpc
import os


def start(sc_port):
    from ..cell import webkit_GUI_hook
    t = open(os.path.join(abs_dir(__file__), "webkit_client_rpc_utils.py"), "rb").read().decode()
    open("webkit_client_rpc_utils.py", "wb").write(t.encode())
    t = open(os.path.join(abs_dir(__file__), "webkit_client_rpc.py"), "rb").read().decode()
    t = t.replace("'<sc_port>'", str(sc_port))
    open("webkit_client_rpc.py", "wb").write(t.encode())
    runShell("python3.7 webkit_client_rpc.py")
    RPC = rpc(sc_port)
    def _screenshot():
        return RPC("utils.screenshot")
    webkit_GUI = webkit_GUI_hook(sc_port, _screenshot=_screenshot, _enable_input=False)
    webkit_GUI.rpc = RPC
    return webkit_GUI

