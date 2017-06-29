from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import socket
import sys

class server_setup(object):
    def __init__(self, file, password=None):
        self.password = password
        self.name = file
        self.file = open(file, "rb").read()

class webpage_setup(object):
    def __init__(self):
        self.logo = open("logo.png", "rb").read()
        self.password = open("pages/password.html").read()
        self.standard = open("pages/standard.html").read()

class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

        if self.path == "/logo.png" or self.path == "/favicon.ico":
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(html.logo)
            return

        elif self.path == user.name:
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(user.file)

        else:
            self.send_header('Content-type', 'text/html')
            if self.path == "/standard":
                if user.password:
                    webpage = html.password
                    webpage = webpage.replace("%identifier%", "password")
                    webpage = webpage.replace("%require_password_info%", "This Flag is password protected!")
                else:
                    webpage = html.standard
                    webpage = webpage.replace("%size_of_file%", str(round(len(user.file)/10000, 2)))
                    webpage = webpage.replace("%name_of_file%", user.name)
            else:
                webpage = "<div style='color:#c9d0e0; font-family:courier new; text-align:center;'><a href='/standard' title='return to /standard page'><img src='logo.png' style='height: 250px; width: 250px;'></a></img><p style='font-size:50px;'>404 Error!</p><br><p style='font-size:25px;'>Page not found...</p></div>"

        self.end_headers()
        self.wfile.write(bytes(webpage, "utf8"))
        return

    def do_POST(self):
        post_length = int(self.headers["Content-Length"])
        post_data = urllib.parse.parse_qs(self.rfile.read(post_length).decode("utf-8"))

        if "password" in post_data and post_data["password"][0] == str(user.password):
            webpage = html.standard
            webpage = webpage.replace("%size_of_file%", str(round(len(user.file)/10000, 2)))
            webpage = webpage.replace("%name_of_file%", user.name)
            print("Succesful connection")
        else:
            webpage = "<div style='color:#c9d0e0; font-family:courier new; text-align:center;'><img src='logo.png' style='height: 250px; width: 250px;'></img><p style='font-size:50px;'>500 Error!</p><br><p style='font-size:25px;'>Access denied!</p></div>"
            print("Unsuccessful connection: Invalid password")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes(webpage, "utf8"))
        return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[0]
        if len(sys.argv) > 2:
            password = sys.argv[1]
        else:
            password = None
    else:
        file_path = input("File path:\n> ")
        password = input("Password (optional):\n> ")
    user = server_setup(file_path, password)
    html = webpage_setup()
    
    local_ip = socket.gethostbyname(socket.gethostname())
    print("local ip: "+local_ip)
    server_address = (local_ip, 8081)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print("server running on localhost:8081/standard")
    httpd.serve_forever()
