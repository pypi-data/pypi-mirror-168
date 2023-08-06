# noinspection PyUnresolvedReferences
from IPython.display import HTML
from unencryptedsocket import SC
# noinspection PyUnresolvedReferences
from google.colab import output
from base64 import b64encode
from uuid import uuid4
import time


def webkit_GUI_hook(sc_port, _enable_input=True):
    def sc():
        return SC(host="127.0.0.1", port=sc_port)


    def add_job(t, v):
        return sc().request(command="add_job", data=((t, v), {}))


    def get_job_result(t):
        r = sc().request(command="get_job_result", data=((t,), {}))
        if isinstance(r, Exception):
            raise KeyError
        return r


    def get_tabs(*args, **kwargs):
        return sc().request(command="get_tabs", data=(args, kwargs))


    def set_tab(*args, **kwargs):
        return sc().request(command="set_tab", data=(args, kwargs))


    def close_tab(*args, **kwargs):
        return sc().request(command="close_tab", data=(args, kwargs))


    def screenshot():
        if stop:
            return
        t = time.time()
        add_job(t, ["screenshot"])
        elapsed = 0
        while elapsed <= 1:
            try:
                return get_job_result(t)
            except:
                time.sleep(1/1000)
                elapsed += 1/1000
        return b"timeout"


    def get_tabs_cb():
        if stop:
            return
        return get_tabs()


    def set_tab_cb(id):
        if stop:
            return
        return set_tab(id)


    def close_tab_cb(id):
        if stop:
            return
        return close_tab(id)


    def test_cb(*args, **kwargs):
        return True


    def mouse_cb(*args):
        if stop:
            return
        args = list(map(int, args))
        t = time.time()
        add_job(t, ["mouse", *args])
        elapsed = 0
        while elapsed <= 1:
            try:
                return get_job_result(t)
            except:
                time.sleep(1/1000)
                elapsed += 1/1000
        return "timeout"


    def wheel_cb(*args):
        if stop:
            return
        args = [int(args[0])]
        t = time.time()
        add_job(t, ["wheel", *args])
        elapsed = 0
        while elapsed <= 1:
            try:
                return get_job_result(t)
            except:
                time.sleep(1/1000)
                elapsed += 1/1000
        return "timeout"


    def keyboard_cb(*args):
        if stop:
            return
        args = [args[0], int(args[1])]
        t = time.time()
        add_job(t, ["keyboard", *args])
        elapsed = 0
        while elapsed <= 1:
            try:
                return get_job_result(t)
            except:
                time.sleep(1/1000)
                elapsed += 1/1000
        return "timeout"


    def screenshot_cb():
        if stop:
            return
        r = screenshot()
        img = b64encode(r).decode()
        # noinspection PyUnresolvedReferences
        display(HTML('''
<script>
(function(){
    let img = document.querySelector('div#prev img');
    img.src = "data:image/jpg;base64,<img>";
    let ti = setInterval(async function(){
        if(img.complete){
            clearInterval(ti);
            let r = await google.colab.kernel.invokeFunction('<update_uuid>', [], {});
            // console.log(r)
        }
    }, 100);
    Array.from(document.querySelectorAll("script")).map(function(e){
        e = e.parentElement.parentElement;
        if(!e.querySelector("div#prev img")) e.remove()
    });
})();
</script>
'''.replace("<update_uuid>", update_uuid)
        .replace("<img>", img)))


    def render():
        # noinspection PyUnresolvedReferences
        display(HTML('''
<style>
div#tabs{
    display: flex;
    justify-content: center;
    align-items: center;
}
div#tabs div[id]{
    padding: 5px 10px;
    border-right: 1px solid white;
    cursor: pointer;
    letter-spacing: -1px;
}
div#tabs div[id]:first-child{
    border-left: 1px solid white;
}
div#prev{
    text-align:center;
}
div#prev img{
    width: 1024px;
    height: auto;
}
div#prev input#kb{
    width:1px;
    height:1px;
}
</style>
<div id="prev">
  <div id="tabs"></div>
  <img/><br/>
  <input id="kb" readonly/>
  </div>
<script>
let input = document.querySelector("input#kb");
let img = document.querySelector('div#prev img');
img.ondragstart = function() { return false; };
async function onmouse(e, d){
    input.focus();
    e.preventDefault();
    e.stopPropagation();
    let b = e.which;
    let x = e.pageX-img.offsetLeft;
    let y = e.pageY-img.offsetTop;
    // console.log([x,y,img.width,img.height,d,b])
    let r = await google.colab.kernel.invokeFunction('<mouse_uuid>', [x,y,img.width,img.height,d,b], {});
    // console.log(r)
}
img.onmouseup = async function(e){
    await onmouse(e, -1);
}
let moving = 0;
img.onmousemove = async function(e){
    if(moving){
        return;
    }
    moving = 1;
    setTimeout(function(){
        moving = 0;
    }, 100);
    await onmouse(e, 0);
}
img.onmousedown = async function(e){
    await onmouse(e, 1);
}
img.onwheel = async function(e){
    input.focus();
    e.preventDefault();
    e.stopPropagation();
    let d = e.deltaY>0?1:0;
    // console.log([d])
    await google.colab.kernel.invokeFunction('<wheel_uuid>', [d], {});
}
async function onkey(e, d){
    input.focus();
    e.preventDefault();
    e.stopPropagation();
    if(e.keyCode>=65&&e.keyCode<=90){
        //console.log([String.fromCharCode(e.keyCode+32), d])
        //let r = await google.colab.kernel.invokeFunction('<keyboard_uuid>', [String.fromCharCode(e.keyCode+32), d], {});
        let r = await google.colab.kernel.invokeFunction('<keyboard_uuid>', [e.key, d], {});
        //console.log(r);
    }
    else if(e.key){
        //console.log([e.key, d])
        let r = await google.colab.kernel.invokeFunction('<keyboard_uuid>', [e.key, d], {});
        //console.log(r);
    }
}
input.onkeyup = async function(e){
    await onkey(e, 0);
}
input.onkeydown = async function(e){
    await onkey(e, 1);
}
async function get_tabs(){
    let r = await google.colab.kernel.invokeFunction('<get_tabs_uuid>', [], {});
    document.querySelector("div#tabs").innerHTML = "";
    // console.log(r)
    let tabs = eval(r.data['text/plain']);
    for(let t of tabs){
        let tab = document.createElement("div");
        tab.id = t[0];
        tab.innerHTML = (t[1].length>30?t[1].slice(0,30)+" ...":t[1])+" <span class='close'>[x]</span>";
        tab.onclick = async function(e){
            //console.log(e.target.id)
            let r = await google.colab.kernel.invokeFunction('<set_tab_uuid>', [parseInt(e.target.id)], {});
            //console.log(r)
        }
        document.querySelector("div#tabs").appendChild(tab);
    }
    Array.from(document.querySelectorAll("div#tabs span.close")).map(function(e){
        e.addEventListener("click", async function(e){
            e.preventDefault();
            e.stopPropagation();
            //console.log(e.target.parentElement.id)
            let r = await google.colab.kernel.invokeFunction('<close_tab_uuid>', [parseInt(e.target.parentElement.id)], {});
            //console.log(r)
        });
    });
    setTimeout(get_tabs, 1000);
}
get_tabs().then(function(){});
</script>
'''.replace("<mouse_uuid>", mouse_uuid)
        .replace("<wheel_uuid>", wheel_uuid)
        .replace("<keyboard_uuid>", keyboard_uuid)
        .replace("<get_tabs_uuid>", get_tabs_uuid)
        .replace("<set_tab_uuid>", set_tab_uuid)
        .replace("<close_tab_uuid>", close_tab_uuid)))
        screenshot_cb()


    stop = False
    update_uuid = str(uuid4())
    mouse_uuid = str(uuid4())
    wheel_uuid = str(uuid4())
    keyboard_uuid = str(uuid4())
    get_tabs_uuid = str(uuid4())
    set_tab_uuid = str(uuid4())
    close_tab_uuid = str(uuid4())
    _screenshot_cb = screenshot_cb
    _mouse_cb = test_cb
    _wheel_cb = test_cb
    _keyboard_cb = test_cb
    _get_tabs_cb = test_cb
    _set_tab_cb = test_cb
    _close_tab_cb = test_cb
    if _enable_input:
        _mouse_cb = mouse_cb
        _wheel_cb = wheel_cb
        _keyboard_cb = keyboard_cb
        _get_tabs_cb = get_tabs_cb
        _set_tab_cb = set_tab_cb
        _close_tab_cb = close_tab_cb
    events_hook = [
        (update_uuid, _screenshot_cb),
        (mouse_uuid, _mouse_cb),
        (wheel_uuid, _wheel_cb),
        (keyboard_uuid, _keyboard_cb),
        (get_tabs_uuid, _get_tabs_cb),
        (set_tab_uuid, _set_tab_cb),
        (close_tab_uuid, _close_tab_cb),
    ]
    for _ in events_hook:
        output.register_callback(*_)
    class _:
        pass
    def _stop():
        nonlocal stop
        stop = True
    def _start():
        nonlocal stop
        stop = False
        render()
    def _rpc(name, *args):
        t = time.time()
        if not args:
            args = [tuple(), dict()]
        add_job(t, [name, *args])
        while time.time() - t < 30:
            try:
                return get_job_result(t)
            except KeyError:
                time.sleep(1 / 1000)
        return "timeout"
    _.start = _start
    _.stop = _stop
    _.rpc = _rpc
    return _


