from __future__ import annotations

import argparse
import functools
import http.server
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the CHECK help application locally")
    parser.add_argument("--directory", type=Path, default=ROOT / "help-dist")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=args.directory)
    server = http.server.ThreadingHTTPServer((args.host, args.port), handler)
    url = f"http://{args.host}:{args.port}/"
    print(f"CHECK 도움말: {url}")
    if not args.no_browser:
        threading.Timer(0.6, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
