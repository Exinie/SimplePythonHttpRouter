from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import os
import mimetypes

from config import IP, PORT, STATIC_DIR
from routes import RouteHandler

routes_and_handlers = RouteHandler()


class RequestHandler(BaseHTTPRequestHandler):

    def send_error_response(self, status, title, message):
        print(status, title, message)
        self.send_response(status)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(f"<html><body><h1>{status} - {title}</h1><p>{message}</p></body></html>".encode('utf-8'))
        return

    def do_GET(self):

        if ("GET", self.path) in routes_and_handlers.ROUTES:
            target_html_file = routes_and_handlers.ROUTES[("GET", self.path)]
            target_html_file_location = os.path.join(STATIC_DIR, target_html_file)

            # Check if the HTML file for the intended route exists
            if os.path.exists(target_html_file_location) and os.path.isfile(target_html_file_location):
                try:
                    # Read file in binary (?)
                    with open(target_html_file_location, 'rb') as file:
                        self.send_response(200)  # Send 200 OK response
                        mimetype, _ = mimetypes.guess_type(target_html_file_location)
                        self.send_header('Content-type', mimetype or "application/octet-stream")
                        self.end_headers()  # Finish header
                        self.wfile.write(file.read())  # Write file as response (?)
                    return
                except Exception as e:
                    # If error while rendering HTML file (500)
                    print(f"GET error: {e}")
                    self.send_error_response(500, "Internal server error", "")
                    return
            else:
                # If HTML file for the intended route is not exist
                self.send_error_response(404, "Not found", "")
                return
        else:
            # If route not exist in ROUTES dictionary
            self.send_error_response(404, "Not found", "")
            return

    def do_POST(self):
        if ("POST", self.path) in routes_and_handlers.ROUTES:
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_body = self.rfile.read(content_length).decode('utf-8')

                # Parsing URL, example output: username=Exinie&password=exinie123!
                post_data = parse_qs(post_body)

                handler = routes_and_handlers.ROUTES[("POST", self.path)]
                handler(post_data)

                # Response
                self.send_response(200)
                self.send_header('Location', '/index.html')
                self.end_headers()
                return
            except Exception as e:
                # If error while rendering HTML file (500)
                print(f"POST error: {e}")
                self.send_error_response(500, "Internal server error", "")
                return
        else:
            self.send_error_response(404, "Not found", "")
            return


def run_server():

    try:
        server = HTTPServer((IP, PORT), RequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" Closing server.")
        server.server_close
    except Exception as e:
        print(f"Error starting server: {e}")


if __name__ == "__main__":
    run_server()
