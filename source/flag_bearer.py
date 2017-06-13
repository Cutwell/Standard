from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import tkinter as tk
import shutil

class server_gui(object):

    def __init__(self):
        self.root = tk.Tk()



class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

        if self.path == "/logo.png":
            self.send_header('Content-type', 'image/png')
            webpage = open("logo.png", "r").read()

        else:
            self.send_header('Content-type', 'text/html')
            if self.path == "/download" or self.path == "/standard":
                webpage = open("pages/standard.html", "r").read()
            else:
                webpage = "<div style='color:#c9d0e0; font-family:courier new; text-align:center;'><img src='logo.png'></img><p style='font-size:50px;'>404 Error!</p><br><p style='font-size:25px;'>Page not found...</p></div>"

        #  write content as utf-8 data
        self.end_headers()
        self.wfile.write(bytes(webpage, "utf8"))
        return

    def do_POST(self):
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        #  dictionary of post data
        post_length = int(self.headers["Content-Length"])
        post_data = urllib.parse.parse_qs(self.rfile.read(post_length).decode("utf-8"))


if __name__ == "__main__":
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print("server running on localhost:8081/")
    httpd.serve_forever()
