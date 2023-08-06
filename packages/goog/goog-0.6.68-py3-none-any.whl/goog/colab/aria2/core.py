# noinspection PyUnresolvedReferences
from mixlab import (
    runSh,
    PortForward_wrapper,
    findProcess,
    findPackageR
)
from urllib.parse import urlparse
import urllib.request
import traceback
import requests
import pathlib
import zipfile
import random
import re
import os


def install():
    runSh("apt install -y aria2")
    pathlib.Path("ariang").mkdir(mode=0o777, exist_ok=True)
    if not os.path.exists("ariang/index.html"):
        urllib.request.urlretrieve(
            findPackageR("mayswind/AriaNg", "AllInOne.zip"),
            "ariang/new.zip"
        )
        with zipfile.ZipFile("ariang/new.zip", "r") as zip_ref:
            zip_ref.extractall("ariang")
        try:
            pathlib.Path("ariang/new.zip").unlink()
        except FileNotFoundError:
            pass


def start(
        save_location = "/mnt/goog",
        rpc_listen_port = 6800,
        on_download_complete = "https://raw.githubusercontent.com/foxe6/MiXLab/master/resources/aria2/on_download_complete.py",
        enable_tunnel=True
):
    try:
        odc = requests.get(on_download_complete).text
        on_download_complete = "/content/" + os.path.basename(on_download_complete)
        open(on_download_complete, "wb").write(odc.encode())
        pathlib.Path(on_download_complete).chmod(0o777)
    except:
        on_download_complete = None
    pathlib.Path(save_location).mkdir(mode=0o777, exist_ok=True)
    if not findProcess("aria2c", "--enable-rpc"):
        try:
            trackers = requests.get(
                "https://trackerslist.com/best_aria2.txt"
            ).text
            cmdC = (r"aria2c --enable-rpc --rpc-listen-port={} -D ".format(rpc_listen_port) +
                    r"-d {} ".format(save_location) +
                    r"-c " +
                    fr"--bt-tracker={trackers} " +
                    r"--bt-request-peer-speed-limit=8M " +
                    r"--bt-max-peers=0 " +
                    r"--seed-ratio=0.0 " +
                    r"--max-upload-limit=2M " +
                    r"--max-download-limit=8M " +
                    r"--max-overall-download-limit=15M " +
                    r"--max-connection-per-server=8 " +
                    r"--max-download-result=100 " +
                    r"--max-concurrent-downloads=1 " +
                    r"--min-split-size=10M " +
                    r"--follow-torrent=false " +
                    r"--disable-ipv6=true " +
                    r"--rpc-allow-origin-all=true " +
                    r"--check-certificate=false " +
                    r"--user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' " +
                    r"--peer-agent=Transmission/2.77 " +
                    r"--peer-id-prefix=-TR2770- " +
                    r"--split=20 " +
                    (r"--on-download-complete='{}'".format(on_download_complete) if on_download_complete else "") +
                    r" &")
            # print(cmdC)
            runSh(cmdC, shell=True)
            if enable_tunnel:
                Server = PortForward_wrapper(
                    "argotunnel",
                    "",
                    True,
                    [["aria2_rpc", rpc_listen_port, "http"]],
                    "jp",
                    ["", random.randint(5000, 5500)]
                )
                data = Server.start("aria2_rpc", displayB=False, v=False)
                return urlparse(data["url"]).hostname
        except:
            print("aria2 RPC cannot be started", traceback.format_exc())


def startWebUI(
        rpc_ip_host,
        web_ui_port = 6801
):
    if not rpc_ip_host:
        raise ValueError("rpc_ip_host")
    filePath = "ariang/index.html"
    with open(filePath, "r+") as f:
        read_data = f.read()
        f.seek(0)
        f.truncate(0)
        read_data = re.sub(r'(rpcHost:"\w+.")|rpcHost:""', 'rpcHost:"{}"'.format(rpc_ip_host), read_data)
        read_data = re.sub(r'protocol:"\w+."', r'protocol:"ws"', read_data)
        read_data = re.sub(r'rpcPort:"\d+."', 'rpcPort:"80"', read_data)
        read_data = re.sub(r"globalStatRefreshInterval:1e3,downloadTaskRefreshInterval:1e3",
                           "globalStatRefreshInterval:5e3,downloadTaskRefreshInterval:5e3", read_data)
        f.write(read_data)
    try:
        urllib.request.urlopen("http://localhost:{}".format(web_ui_port))
    except:
        runSh("python3 -m http.server {} &".format(web_ui_port), shell=True, cd="ariang/")
    Server = PortForward_wrapper(
        "argotunnel",
        "",
        True,
        [["ariang", web_ui_port, "http"]],
        "jp",
        ["", random.randint(5000, 5500)]
    )
    data = Server.start("ariang", displayB=False, v=False)
    return urlparse(data["url"])._replace(scheme="http").geturl()

