import os
import sys
from subprocess import run


sys.path.insert(0, "/root/.ipython")
if not os.path.exists("/root/.ipython/mixlab.py"):
    from shlex import split as _spl

    shellCmd = "wget -qq https://raw.githubusercontent.com/foxe6/MiXLab/master/resources/mixlab.py \
                    -O /usr/local/lib/python3.7/dist-packages/mixlab.py"
    run(_spl(shellCmd))  # nosec


