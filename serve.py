#!/usr/bin/env python3
"""Static file server for the demo with no-cache headers (so a rebuild is
picked up on reload without cache busting)."""
import http.server
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8099


class DemoHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()


if __name__ == "__main__":
    http.server.test(HandlerClass=DemoHandler, port=PORT)
