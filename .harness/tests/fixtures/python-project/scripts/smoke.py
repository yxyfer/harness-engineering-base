from pathlib import Path
from http.client import HTTPConnection
import os
import selectors
import subprocess
import sys

root = Path(__file__).parents[1]
environment = {**os.environ, "PORT": "0"}
process = subprocess.Popen(
    [sys.executable, "app.py"], cwd=root, env=environment,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
)
try:
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    if not selector.select(timeout=3):
        raise RuntimeError("example server did not become ready")
    line = process.stdout.readline().strip()
    if not line.startswith("http://127.0.0.1:"):
        error = process.stderr.read().strip()
        raise RuntimeError(error or "example server did not report its URL")
    port = int(line.rsplit(":", 1)[1])
    connection = HTTPConnection("127.0.0.1", port, timeout=2)
    connection.request("GET", "/")
    response = connection.getresponse()
    body = response.read()
    connection.close()
    if response.status != 200:
        raise RuntimeError(f"unexpected HTTP status: {response.status}")
    if b"Harness ready" not in body:
        raise RuntimeError("golden-path content was not returned")
    print("smoke: pass")
finally:
    process.terminate()
    process.wait(timeout=2)
