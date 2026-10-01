from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from example_app.message import page_html


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = page_html()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format: str, *_args: object) -> None:
        return


if __name__ == "__main__":
    address = ("127.0.0.1", int(os.environ.get("PORT", "8000")))
    server = HTTPServer(address, Handler)
    print(f"http://127.0.0.1:{server.server_port}", flush=True)
    server.serve_forever()
