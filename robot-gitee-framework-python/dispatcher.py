from http.server import HTTPServer, BaseHTTPRequestHandler

class Webhook(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/gitee-hook":
            self.send_error(400, "Bad Request: unknown path")
            return

        if self.headers.get("User-Agent") != "Robot-Gitee-Access":
            self.send_error(400, "Bad Request: unknown User-Agent Header")
            return

        event_type = self.headers.get("X-Gitee-Event"); 
        if event_type == "":
            self.send_error(400, "Bad Request: Missing X-Gitee-Event Header")
            return

        uuid = self.headers.get("X-Gitee-Timestamp")
        if uuid == "":
            self.send_error(400, "Bad Request: Missing X-Gitee-Timestamp Header")
            return

        data = self.rfile.read(int(self.headers.get("content-length")))

        print(event_type)
        print(uuid)
        print(data)
        print(self.server.handlers)

        self.server.dispatch(event_type, uuid, data)

        self.send_response_only(201, "done")

    def do_GET(self):
        if self.path != "/":
            self.send_error(400, "Bad Request: unknown path")
            return

        self.send_response_only(200, "done")


class Dispatcher(HTTPServer):
    def __init__(self, server_address, handlers):
        self.handlers = handlers

        super().__init__(server_address, Webhook)

    def run():
        print("start server, listen on: %s:%d" % self.server_address)

        try:
            server.serve_forever()
        finally:
            print("shutdown the server")
            server.shutdown()
            print("server is shutdown")

            # wait threads to exit

    def dispatch(self, event_type, uuid, payload):
        if event_type not in self.handlers:
            return

        self.handlers[event_type](payload)
