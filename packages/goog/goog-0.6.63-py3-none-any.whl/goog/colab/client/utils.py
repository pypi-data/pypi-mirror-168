from unencryptedsocket import SC
import time



def rpc(sc_port):
    def add_job(t, name, *args, **kwargs):
        return SC(host="127.0.0.1", port=sc_port).request(command="add_job", data=((t, (name, args, kwargs)), {}))


    def get_job_result(t):
        r = SC(host="127.0.0.1", port=sc_port).request(command="get_job_result", data=((t,), {}))
        if isinstance(r, KeyError):
            raise r
        return r

    def _(name, *args, **kwargs):
        t = time.time()
        add_job(t, name, *args, **kwargs)
        while time.time()-t<30:
            try:
                return get_job_result(t)
            except KeyError:
                time.sleep(1/1000)
        return "timeout"
    return _

