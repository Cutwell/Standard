from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import tkinter as tk
import shutil
import pyre
import random
import hashlib

class server_gui(object):

    def __init__(self):
        pyre.Pyre()
        pyre.print("Standard setup:")
        self.username = pyre.input("Enter Flag name")
        self.password = pyre.input("Enter Passcode (optional)")
        pyre.pyre_root.withdraw()

        # create the upload var, so we can access it from any instance of the HTTPServer_RequestHandler class
        self.upload = ""

    def main(self):
        self.root = tk.Tk()


    def gen_secure_key(self):
        string = (self.username+str(random.random())).encode('UTF-8')
        hash_object = hashlib.sha1(string)
        hash_dig = list(hash_object.hexdigest())
        self.secure_key = "".join(hash_dig[:6])
        print("New Secure Key (use to access the /upload webpage): "+self.secure_key)


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

        if self.path == "/logo.png" or self.path == "/favicon.ico":
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(open("logo.png", "rb").read())
            return

        elif self.path == "/download":
            with open("/upload/flag.txt") as fh:
                self.send_header('Content-type', 'application/zip')
                self.end_headers()
                self.wfile.write(fh.read().encode())

        else:
            self.send_header('Content-type', 'text/html')
            if self.path == "/standard":
                if gui.password:
                    webpage = open("pages/password.html").read()
                    webpage = webpage.replace("%identifier%", "password")
                    webpage = webpage.replace("%require_password_info%", "This Flag is password protected!")
                else:
                    webpage = open("pages/standard.html", "r").read()
                    webpage = webpage.replace("%user_name%", gui.username)
                    webpage = webpage.replace("%path_to_file%", gui.upload)
                    webpage = webpage.replace("%size_of_file%", str(len(gui.upload)/1000000))
                    webpage = webpage.replace("%name_of_file%", gui.upload)

            elif self.path == "/upload":
                webpage = open("pages/password.html").read()
                webpage = webpage.replace("%identifier%", "secure_key")
                webpage = webpage.replace("%require_password_info%", "This area is restricted!")

            else:
                webpage = "<div style='color:#c9d0e0; font-family:courier new; text-align:center;'><a href='/standard' title='return to /standard page'><img src='logo.png' style='height: 250px; width: 250px;'></a></img><p style='font-size:50px;'>404 Error!</p><br><p style='font-size:25px;'>Page not found...</p></div>"

        self.end_headers()
        self.wfile.write(bytes(webpage, "utf8"))
        return

    def do_POST(self):
        post_length = int(self.headers["Content-Length"])
        post_data = urllib.parse.parse_qs(self.rfile.read(post_length).decode("utf-8"))

        # security feature
        if "secure_key" in post_data and post_data["secure_key"][0] != str(gui.secure_key):
            print("Bad Login: User attempted to access /upload page with bad secure_key")
            gui.gen_secure_key()
            webpage = "<div style='color:#c9d0e0; font-family:courier new; text-align:center;'><img src='logo.png' style='height: 250px; width: 250px;'></img><p style='font-size:50px;'>500 Error!</p><br><p style='font-size:25px;'>Access denied!</p></div>"
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(webpage, "utf8"))
            return

        if "password" in post_data and post_data["password"][0] == str(gui.password):
            webpage = open("pages/standard.html", "r").read()
            webpage = webpage.replace("%user_name%", gui.username)
            webpage = webpage.replace("%path_to_file%", gui.upload)
            webpage = webpage.replace("%size_of_file%", str(len(gui.upload)/1000000))
            webpage = webpage.replace("%name_of_file%", gui.upload)

        elif "secure_key" in post_data and post_data["secure_key"][0] == str(gui.secure_key):
            webpage = open("pages/upload.html").read()
            gui.gen_secure_key()

        elif "file" in post_data:
            length = int(self.headers['content-length'])
            data = self.rfile.read(length)

            with open("/upload/flag.txt", 'w') as file:
                file.write(data.decode())

            webpage = "<div style='color:#c9d0e0; font-family:courier new; text-align:center;'><img src='logo.png' style='height: 250px; width: 250px;'></img><p style='font-size:50px;'>Upload Succesful!</p><br><p style='font-size:25px;'>Visit /standard to access the file for download</p></div>"

        else:
            webpage = "<div style='color:#c9d0e0; font-family:courier new; text-align:center;'><img src='logo.png' style='height: 250px; width: 250px;'></img><p style='font-size:50px;'>500 Error!</p><br><p style='font-size:25px;'>Access denied!</p></div>"

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes(webpage, "utf8"))
        return

if __name__ == "__main__":
    gui = server_gui()
    gui.gen_secure_key()
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print("server running on localhost:8081/")
    httpd.serve_forever()
