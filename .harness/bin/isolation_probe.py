"""Native direct-egress denial and necessary synthetic loopback assertions."""

import errno
import json
import os
import socket
import subprocess
import sys
import urllib.error
import urllib.request


def denied():
    # TEST-NET-2, not a real provider/production service. EPERM establishes OS
    # denial; timeout, DNS failure or connection refusal are NOT isolation proof.
    with socket.socket() as client:
        client.settimeout(1)
        try:
            client.connect(("198.51.100.42", 443))
        except OSError as error:
            if error.errno not in {errno.EPERM, errno.EACCES}:
                raise AssertionError(
                    "egress was not denied by external policy"
                ) from error
        else:
            raise AssertionError("non-loopback egress unexpectedly allowed")


if __name__ == "__main__":
    denied()
    if "--child" not in sys.argv:
        subprocess.run(
            [sys.executable, __file__, "--child"], check=True, timeout=5
        )
        # Real HTTP client attempts at a documentation-only IP: no production
        # or provider hostname is contacted, and no real credentials exist.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        for path in ("/production", "/v1/chat/completions"):
            try:
                opener.open("http://198.51.100.42" + path, timeout=1)
            except urllib.error.URLError as error:
                assert isinstance(error.reason, OSError)
                assert error.reason.errno in {errno.EPERM, errno.EACCES}
            else:
                raise AssertionError(
                    "synthetic production/provider attempt escaped"
                )
        with socket.socket() as server, socket.socket() as client:
            server.bind(("127.0.0.1", 0))
            server.listen(1)
            client.settimeout(2)
            client.connect(server.getsockname())
            accepted, _ = server.accept()
            with accepted:
                client.sendall(b"synthetic")
                assert accepted.recv(64) == b"synthetic"
        assert os.environ.get("HARNESS_ENVIRONMENT") == "synthetic"
        assert not any(
            k in os.environ
            for k in (
                "OPENAI_API_KEY",
                "ANTHROPIC_API_KEY",
                "AWS_SECRET_ACCESS_KEY",
                "NODE_OPTIONS",
            )
        )
        print(
            json.dumps(
                {
                    "direct_egress": "denied",
                    "child_egress": "denied",
                    "loopback": "passed",
                    "environment": "synthetic",
                }
            )
        )
