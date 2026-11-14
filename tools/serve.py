"""Local preview server that behaves like Cloudflare Pages for this site.

    python tools/serve.py [port]

Serves the project folder, applies the global headers from _headers
(including the Content-Security-Policy, so violations show in the browser
console), serves 404.html for missing pages, and returns a stub reply for
POST /api/inquiry (the real handler only runs on Cloudflare).
"""
import http.server, os, sys, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

def global_headers():
    out, active = [], False
    with open(os.path.join(ROOT, "_headers"), encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            if not line[0].isspace():
                active = line.strip() == "/*"
                continue
            if active:
                k, v = line.strip().split(":", 1)
                if k != "Strict-Transport-Security":
                    out.append((k, v.strip().replace(" upgrade-insecure-requests", "").rstrip(";")))
    return out

HEADERS = global_headers()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        for k, v in HEADERS:
            self.send_header(k, v)
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            body = open(os.path.join(ROOT, "404.html"), "rb").read()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().send_error(code, message, explain)

    def do_POST(self):
        if self.path.startswith("/api/inquiry"):
            body = json.dumps({"ok": False, "error": "Local preview: the form only sends on Cloudflare."}).encode()
            self.send_response(503)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(405)

if __name__ == "__main__":
    print(f"Serving {ROOT} at http://localhost:{PORT}")
    http.server.ThreadingHTTPServer(("", PORT), Handler).serve_forever()
