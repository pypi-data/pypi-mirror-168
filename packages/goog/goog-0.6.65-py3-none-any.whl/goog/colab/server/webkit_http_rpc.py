from http.server import BaseHTTPRequestHandler, HTTPServer
from unencryptedsocket import SC
import json
import time


def client_add_job(t, name, *args, **kwargs):
    return SC(host="127.0.0.1", port='<sc_port>').request(command="add_job", data=((t, (name, args, kwargs)), {}))


def client_get_job_result(t):
    return SC(host="127.0.0.1", port='<sc_port>').request(command="get_job_result", data=((t,), {}))


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(data_string)
        t = time.time()
        client_add_job(t, data[0], *data[1], **data[2])
        elapsed = 0
        while True:
            r = client_get_job_result(t)
            if not isinstance(r, Exception):
                break
            time.sleep(1/1000)
            elapsed += (1/1000)
            if elapsed > 1:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"timeout")
                return
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(r).encode())


with HTTPServer(('127.0.0.1', '<port>'), handler) as server:
    server.serve_forever()


