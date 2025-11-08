"""
Simple HTTP server that returns the MD5 hash of the request body.

启动示例:
    if __name__ == "__main__":
        run_md5_http_server()
"""

from __future__ import annotations

import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Tuple
from urllib.parse import parse_qs


class _MD5RequestHandler(BaseHTTPRequestHandler):
    """Handles POST requests by returning the MD5 digest of the body."""

    server_version = "MD5HTTP/0.1"

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        # Reduce noise when embedding this server into other scripts.
        return

    def do_GET(self) -> None:  # noqa: N802
        """Provide a tiny helper page so browsers can interact."""
        page = """\
<html>
  <head>
    <style>
      body { font-family: sans-serif; font-size: 20px; padding: 2rem; }
      input, button { font-size: 20px; padding: 0.3rem 0.5rem; }
    </style>
  </head>
  <body>
    <form method="post">
      <label>Payload:</label>
      <input name="data" />
      <button type="submit">Hash</button>
    </form>
  </body>
</html>
"""
        encoded = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self) -> None:  # noqa: N802  (http.server naming)
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)
        content_type = self.headers.get("Content-Type", "")

        is_form = content_type.startswith("application/x-www-form-urlencoded")
        if is_form:
            decoded = raw_body.decode("utf-8")
            payload_text = parse_qs(decoded).get("data", [""])[0]
            payload = payload_text.encode("utf-8")
        else:
            payload = raw_body

        digest = hashlib.md5(payload, usedforsecurity=False).hexdigest()

        if is_form:
            response_body = f"""\
<html>
  <head>
    <style>
      body {{ font-family: sans-serif; font-size: 24px; padding: 2rem; }}
      .hash {{ font-weight: bold; font-size: 32px; word-break: break-all; }}
      a {{ font-size: 18px; }}
    </style>
  </head>
  <body>
    <p>MD5 digest:</p>
    <div class="hash">{digest}</div>
    <p><a href="/">Back</a></p>
  </body>
</html>
"""
            response = response_body.encode("utf-8")
            content_type_header = "text/html; charset=utf-8"
        else:
            response = digest.encode("ascii")
            content_type_header = "text/plain; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", content_type_header)
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


def run_md5_http_server(
    host: str = "0.0.0.0",
    port: int = 8000,
) -> HTTPServer:
    """
    Start a blocking HTTP server that returns MD5 hashes of POST request bodies.

    Args:
        host: Bind address.
        port: Listening port.

    Returns:
        The running `HTTPServer` instance (main thread blocks until interrupted).
    """

    server_address: Tuple[str, int] = (host, port)
    httpd = HTTPServer(server_address, _MD5RequestHandler)
    print(f"Serving MD5 endpoint on http://{host}:{port} (POST body to hash)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        httpd.server_close()
    return httpd


if __name__ == "__main__":
    run_md5_http_server()
