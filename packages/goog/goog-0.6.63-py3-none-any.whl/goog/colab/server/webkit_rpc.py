from unencryptedsocket import SS
from playwright.sync_api import sync_playwright
import threading
import time
import json
import os


def handle_popup(page):
    add_page_handlers(page)


def add_page_handlers(page):
    page.on("popup", handle_popup)


def add_job(t, v):
    jobs[t] = v
    return True


def get_job_result(t):
    try:
        return job_results.pop(t)
    except:
        return KeyError()


jobs = {}
job_results = {}
with sync_playwright() as pw:
    driver = pw.webkit.launch(
        timeout=5000,
        headless=True,
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
    o_new_page = context.new_page
    def new_page():
        page = o_new_page()
        add_page_handlers(page)
        return page
    context.new_page = new_page
    page = context.new_page()
    page.goto("https://google.com/?q=colab")
    ss = SS(
        host="127.0.0.1",
        port='<sc_port>',
        silent=True,
        functions=dict(
            add_job=add_job,
            get_job_result=get_job_result,
        ),
    )
    p = threading.Thread(target=lambda: ss.start())
    p.daemon = True
    p.start()
    while True:
        try:
            t = next(iter(jobs.keys()))
            v = jobs.pop(t)
            name, args, kwargs = v
            try:
                names = name.split(".")
                if names[0] not in ["driver", "context", "page"]:
                    raise UnboundLocalError(names[0])
                method = globals()[names[0]]
                for name in names[1:]:
                    method = getattr(method, name)
                r = method
                if callable(r):
                    r = r(*args, **kwargs)
                try:
                    not isinstance(r, bytes) and json.dumps(r)
                except:
                    r = str(r)
            except Exception as e:
                r = e
            job_results[t] = r
        except:
            time.sleep(1/1000)
    ss.stop()
    driver.close()

