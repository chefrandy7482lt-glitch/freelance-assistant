from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime

TASKS = []


class Handler(BaseHTTPRequestHandler):

    def _send(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == "/tasks":
            self._send(TASKS)
        else:
            self._send({"status": "online"})

    def do_POST(self):
        if self.path == "/tasks":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode()

            data = json.loads(body)
            task = data.get("task", "")

            TASKS.append({
                "task": task,
                "created": str(datetime.now())
            })

            self._send({"status": "added", "task": task})


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("RUNNING")
    server.serve_forever()