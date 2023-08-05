from playwright.sync_api import sync_playwright
from unencryptedsocket import SS
import traceback
import threading
import inspect
import json
import time
import os
import re


def show_exception(o):
    def _(*args, **kwargs):
        try:
            return o(*args, **kwargs)
        except:
            import traceback
            print(o, args, kwargs, traceback.format_exc())
    return _


def handle_popup(first_page, page):
    add_page_handlers(first_page, page)


def add_page_handlers(first_page, page):
    url = page.url
    if url.startswith("http"):
        page.close()
        goto(first_page, url)
    else:
        page.on("popup", lambda page: handle_popup(first_page, page))


def save_storage_state(context):
    open("auth.json", "wb").write(json.dumps(context.storage_state(), indent=2).encode())


def _add_job(jobs):
    def _(t, v):
        jobs[t] = v
        return True
    return _


def _get_job_result(job_results):
    def _(t):
        try:
            return job_results.pop(t)
        except:
            return KeyError()
    return _


def wait(page, selector, timeout=10):
    t = time.time()
    while time.time()-t<timeout:
        if ":visible" in selector:
            r = page.evaluate("()=>{{let e=document.querySelector(`{}`);return !!(e&&e.offsetParent);}}".format(selector.replace(":visible", "")))
        else:
            r = page.evaluate("()=>!!document.querySelector(`{}`)".format(selector))
        if r:
            return True
        page.wait_for_timeout(100)
    return False


def goto(page, url, retry=5):
    for _ in range(0, retry):
        try:
            page.goto(url)
            return True
        except:
            time.sleep(1)
    raise RuntimeError("goto", url)


def login():
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
        page = context.new_page()
        goto(page, "https://google.com/?q=colab")
        if input("done? "):
            save_storage_state(context)
        driver.close()


def call_utils(driver, context, page, names, args, kwargs, _locals_cache=[0, {}]):
    _globals = dict(driver=driver, context=context, page=page)
    if not _locals_cache[0] or time.time()>os.path.getmtime("webkit_client_rpc_utils.py"):
        _locals_cache[0] = os.path.getmtime("webkit_client_rpc_utils.py")
        _locals_cache[1].clear()
        _locals_cache[1].update(_globals)
        c = open("webkit_client_rpc_utils.py", "rb").read().decode().splitlines()
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


def rpc(driver, context, page, jobs, job_results, startSS):
    goto(page, "https://colab.research.google.com/")
    startSS()
    while True:
        try:
            k = next(iter(jobs.keys()))
            v = jobs.pop(k)
            name, args, kwargs = v
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
                open("error.log", "wb").write(r.encode())
            job_results[k] = r
            page.wait_for_timeout(100)
        except StopIteration:
            page.wait_for_timeout(10)


def main(sc_port):
    if not os.path.isfile("auth.json"):
        for _ in range(0, 5):
            try:
                login()
                break
            except:
                if _ == 4:
                    raise
    jobs = dict()
    job_results = dict()
    add_job = _add_job(jobs)
    get_job_result = _get_job_result(job_results)
    def startSS():
        ss = SS(host="127.0.0.1", port=sc_port, silent=True, functions=dict(
            get_job_result=get_job_result,
            add_job=add_job,
        ))
        p = threading.Thread(target=lambda: ss.start())
        p.daemon = True
        p.start()
    with sync_playwright() as pw:
        driver = pw.webkit.launch(
            timeout=5000,
            headless=True,
        )
        context = driver.new_context(
            locale="en-US",
            timezone_id="America/Phoenix",
            viewport={"width": 1200, "height": 900},
            ignore_https_errors=True,
            bypass_csp=True,
            color_scheme="dark",
            storage_state="auth.json",
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
        rpc(driver, context, page, jobs, job_results, startSS)
    driver.stop()


if __name__ == "__main__":
    main('<sc_port>')

