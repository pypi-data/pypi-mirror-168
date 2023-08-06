from subprocess import Popen, PIPE


def runShell(cmd, **kwargs):
    return Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True, **kwargs)

