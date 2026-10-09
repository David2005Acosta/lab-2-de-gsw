#!/usr/bin/env python3
"""API minima de "Dulce Hogar" (Unidad 1).

Se ejecuta en 127.0.0.1:9000 y es consumida a traves del Reverse Proxy
de Apache configurado en la Fase 3 del laboratorio.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json


class Handler(BaseHTTPRequestHandler):
    def _json(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/saludo":
            nombre = parse_qs(parsed.query).get("nombre", ["invitado"])[0]
            self._json(200, {
                "mensaje": f"Hola {nombre}, bienvenido a Dulce Hogar",
                "servicio": "API Unidad 1",
                "puerto": 9000,
            })
        elif parsed.path == "/api/health":
            self._json(200, {"status": "OK", "servicio": "dulcehogar-api"})
        else:
            self._json(404, {"error": "Ruta no encontrada", "ruta": parsed.path})

    def log_message(self, fmt, *args):
        return


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 9000), Handler).serve_forever()
