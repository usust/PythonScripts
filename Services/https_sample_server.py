"""
HTTPS variant of the MD5 hashing server defined in http_sample_server.py.

Usage:
    python https_sample_server.py --cert cert.pem --key key.pem

Generate a quick self-signed cert:
    openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365
"""

from __future__ import annotations

import argparse
import ssl
from http.server import HTTPServer
from typing import Optional, Tuple

from http_sample_server import _MD5RequestHandler


def run_md5_https_server(
    host: str = "0.0.0.0",
    port: int = 8443,
    certfile: str = "cert.pem",
    keyfile: Optional[str] = None,
) -> HTTPServer:
    """
    Start an HTTPS server that mirrors the HTTP MD5 hashing behavior.

    Args:
        host: Bind address.
        port: Listening port (default 8443).
        certfile: Path to the PEM certificate file (may include private key).
        keyfile: Optional private key file if `certfile` does not contain it.

    Returns:
        Running HTTPServer instance (blocks until interrupted).
    """

    server_address: Tuple[str, int] = (host, port)
    httpd = HTTPServer(server_address, _MD5RequestHandler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"Serving HTTPS MD5 endpoint on https://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping HTTPS server...")
    finally:
        httpd.server_close()
    return httpd


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HTTPS MD5 hashing server")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address (default 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8443, help="Listening port (default 8443)")
    parser.add_argument("--cert", default="cert.pem", help="PEM certificate file")
    parser.add_argument("--key", default="key.pem", help="Private key file (if not in cert)")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    run_md5_https_server(host=args.host, port=args.port, certfile=args.cert, keyfile=args.key)
