import asyncio
from PIL import Image
from io import BytesIO
import time
import json
import sys
import os
import random
import threading
from playwright.sync_api import sync_playwright
from unencryptedsocket import SS, SC


def playwright_worker():
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
                        open("auth.json", "wb").write(json.dumps(context.storage_state(), indent=2).encode())
                        result = "ok"
                    elif v == "get_storage_state":
                        result = context.storage_state()
                    else:
                        raise
                except:
                    import traceback
                    result = traceback.format_exc()
                    traceback.print_exc()
                job_results[t] = result
            except StopIteration:
                time.sleep(1/1000)
            except:
                import traceback
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


