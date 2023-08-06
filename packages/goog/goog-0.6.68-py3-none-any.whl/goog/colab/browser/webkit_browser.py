import asyncio
from PIL import Image
from io import BytesIO
import time
import json
import sys
import os
import random
import traceback
import inspect
import re
import threading
from playwright.sync_api import sync_playwright
from unencryptedsocket import SS, SC


def save_storage_state(context):
    open("auth.json", "wb").write(json.dumps(context.storage_state(), indent=2).encode())


def goto(page, url, retry=5):
    for _ in range(0, retry):
        try:
            page.goto(url)
            return True
        except:
            time.sleep(1)
    raise RuntimeError("goto", url)


def login():
    def handle_popup(first_page, page):
        add_page_handlers(first_page, page)
    def add_page_handlers(first_page, page):
        url = page.url
        if url.startswith("http"):
            page.close()
            goto(first_page, url)
        else:
            page.on("popup", lambda page: handle_popup(first_page, page))
    with sync_playwright() as pw:
        driver = pw.webkit.launch(
            timeout=5000,
            headless=True,
        )
        context = driver.new_context(
            locale="en-US",
            timezone_id="America/Phoenix",
            viewport={"width": 1280, "height": 1000},
            ignore_https_errors=True,
            bypass_csp=True,
            color_scheme="dark",
        )
        o_new_page = context.new_page
        def new_page():
            page = o_new_page()
            add_page_handlers(first_page, page)
            return page
        context.new_page = new_page
        first_page = o_new_page()
        page = first_page
        add_page_handlers(first_page, page)
        goto(page, "https://google.com/?q=colab")
        if input("done?[y] "):
            save_storage_state(context)
        driver.close()


def call_utils(driver, context, page, names, args, kwargs, _locals_cache=[0, {}]):
    _globals = dict(driver=driver, context=context, page=page)
    if not os.path.isfile("webkit_browser_utils.py"):
        raise FileNotFoundError("webkit_browser_utils.py")
    if not _locals_cache[0] or time.time()>os.path.getmtime("webkit_browser_utils.py"):
        _locals_cache[0] = os.path.getmtime("webkit_browser_utils.py")
        _locals_cache[1].clear()
        _locals_cache[1].update(_globals)
        c = open("webkit_browser_utils.py", "rb").read().decode().splitlines()
        for _ in range(1, 4):
            c[_] = ""
        c = "\n".join(c)
        # c = re.sub(r"(^def [a-z_]+\()([^\)])", r"\g<1>driver: Browser, context: BrowserContext, page: Page, \g<2>", c,
        #            flags=re.MULTILINE)
        # c = re.sub(r"(^def [a-z_]+\()(\))", r"\g<1>driver: Browser, context: BrowserContext, page: Page\g<2>", c,
        #            flags=re.MULTILINE)
        exec(c, _locals_cache[1], _locals_cache[1])
    _locals = _locals_cache[1]
    def process(v):
        v = re.sub(r"driver:.*?Page(, )?", "", str(inspect.signature(v))[1:-1])
        if not v:
            return []
        v = v.split(": ")
        _v = [[", ".join(_.split(", ")[:-1]), _.split(", ")[-1]] for i, _ in enumerate(v[1:-1]) if i%2==0]
        _v = [_ for __ in _v for _ in __]
        _v = [v[0]]+_v+[v[-1]]
        v = []
        for i, _ in enumerate(_v):
            if i%2==1:
                v.append([_v[i-1], _v[i]])
        return v
    utils_name = {k: process(v) for k, v in _locals.items() if re.search(r"^[a-z][a-z_]*?[a-z]$", k) and k not in _globals.keys() and "delay" not in k}
    if names[1] == "__list":
        r = utils_name
    else:
        if names[1] not in utils_name:
            raise NameError(names[1])
        else:
            method = _locals[names[1]]
            r = method(*args, **kwargs)
    return r


def playwright_worker(require_session=False):
    if require_session and not os.path.isfile("auth.json"):
        for _ in range(0, 5):
            try:
                login()
                break
            except:
                if _ == 4:
                    raise
    global tabs
    global tabs_lock
    def handle_popup(page):
        add_page_handlers(page)
    def add_page_handlers(page):
        global tab_index
        global tabs_lock
        global tabs
        with tabs_lock:
            tabs[tab_index] = page
            tab_index += 1
        page.on("popup", handle_popup)
    with sync_playwright() as pw:
        driver = pw.webkit.launch(
            timeout=5000,
            headless= True,
        )
        if os.path.isfile("auth.json"):
            storage_state = "auth.json"
        else:
            storage_state = None
        context = driver.new_context(
            locale="en-US",
            timezone_id="America/Phoenix",
            viewport={"width": 1920, "height": 1200},
            ignore_https_errors=True,
            bypass_csp=True,
            color_scheme="dark",
            storage_state=storage_state,
        )
        context.storage_state()
        page = context.new_page()
        add_page_handlers(page)
        page.goto("https://google.com/?q=colab")
        while True:
            try:
                with tabs_lock:
                    for _ in tbc_tabs:
                        tab = tabs.pop(_)
                        tab.close()
                tbc_tabs.clear()
                with tabs_lock:
                    for k in list(tabs.keys()):
                        v = tabs[k]
                        if v.is_closed():
                            tabs.pop(k)
                if ctab in tabs:
                    page = tabs[ctab]
                else:
                    if tabs:
                        page = next(iter(tabs.values()))
                    else:
                        page = context.new_page()
                        add_page_handlers(page)
                        page.goto("https://duckduckgo.com")
                t = next(iter(jobs.keys()))
                v = jobs.pop(t)
                args = v[1:]
                v = v[0]
                try:
                    if v == "screenshot":
                        img = page.screenshot(type="jpeg", quality=100)
                        img = Image.open(BytesIO(img))
                        img = img.convert("RGB")
                        try:
                            LANCZOS = Image.Resampling.LANCZOS
                        except:
                            LANCZOS = Image.LANCZOS
                        img = img.resize(tuple(map(lambda x: int(x*0.75), img.size)), resample=LANCZOS)
                        im = BytesIO()
                        img.save(im, format="JPEG", quality=66, subsampling="4:2:0", optimize=True, progressive=True)
                        result = im.getvalue()
                    elif v == "mouse":
                        x,y,w,h,d,b = args
                        width = page.viewport_size["width"]
                        height = page.viewport_size["height"]
                        x = width*x/w
                        y = height*y/h
                        page.mouse.move(x, y)
                        if d == 1:
                            page.mouse.down(button="left" if b == 1 else "right")
                        elif d == -1:
                            page.mouse.up(button="left" if b == 1 else "right")
                        result = "ok"
                    elif v == "wheel":
                        d, = args
                        page.evaluate("window.scrollTo((document.body.scrollLeft||window.scrollX), (document.body.scrollTop||window.scrollY){}100);".format(
                            "+" if d else "-"
                        ))
                        result = "ok"
                    elif v == "keyboard":
                        k,d = args
                        if d == 1:
                            page.keyboard.down(k)
                        else:
                            page.keyboard.up(k)
                        result = "ok"
                    elif v == "save_storage_state":
                        save_storage_state(context)
                        result = "ok"
                    elif v == "get_storage_state":
                        result = context.storage_state()
                    else:
                        if len(args) != 2:
                            raise
                        name = v
                        args, kwargs = args
                        try:
                            names = name.split(".")
                            if names[0] not in ["driver", "context", "page", "utils"]:
                                raise UnboundLocalError(names[0])
                            if names[0] == "utils":
                                r = call_utils(driver, context, page, names, args, kwargs)
                            else:
                                method = locals()[names[0]]
                                for name in names[1:]:
                                    method = getattr(method, name)
                                r = method
                                if callable(r):
                                    r = r(*args, **kwargs)
                                try:
                                    not isinstance(r, bytes) and json.dumps(r)
                                except:
                                    r = str(r)
                            save_storage_state(context)
                        except:
                            r = traceback.format_exc()
                        result = r
                except:
                    result = traceback.format_exc()
                    traceback.print_exc()
                job_results[t] = result
            except StopIteration:
                time.sleep(1/1000)
            except:
                traceback.print_exc()
                time.sleep(1/1000)
        driver.close()


jobs = dict()
job_results = dict()
tab_index = 0
tabs = {}
tabs_lock = threading.Lock()
ctab = 0
tbc_tabs = []


def close_tab(id):
    tbc_tabs.append(id)
    return True


def set_tab(id):
    global ctab
    ctab = id
    return True


def get_tabs():
    return [[k, v.url] for k, v in tabs.items()]


def add_job(t, v):
    global jobs
    jobs[t] = v
    return True


def get_job_result(t):
    try:
        return job_results.pop(t)
    except:
        return KeyError()


ss = SS(host="127.0.0.1", port='<sc_port>', silent=True, functions=dict(
    close_tab=close_tab,
    set_tab=set_tab,
    get_tabs=get_tabs,
    get_job_result=get_job_result,
    add_job=add_job,
))
p = threading.Thread(target=lambda: ss.start())
p.daemon = True
p.start()
playwright_worker()


