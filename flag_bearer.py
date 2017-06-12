import sys
import socket
import threading
import urllib.request

'''
Usage:
 - Passing an IP and a path will save the file to the path.
 - Passing an IP will seek a server at that address.
 - Passing a path will post a server offering that file.
Security:
 - Posting a server with a password will require connections to pass that password as ID.
 - Seeking a server with password protection will require a passed password to connect.
'''

#  server errors
class FailedToPost(Exception):
    pass

class IncorrectPasscode(Exception):
    pass

#  client errors
class FailedToLocateIP(Exception):
    pass

class FailedToSeek(Exception):
    pass

class standard:

    #  class for "raising" the file to a port and listen for a connection
    #  before sending the file

    #  or for seeking an IP and recieving a file

    def __init__(self, port=500, path=None, ip=None, passcode=None):

        if path != None:
            with open(path, "r") as file:
                self.file = file.read()

        self.ip = ip
        self.passcode = passcode
        self.port = port
        self.external_ip = urllib.request.urlopen('http://ident.me').read().decode('utf8')


    def listen(self):

        #  listen at a defined port for connections

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #  creates a socket object

        server_address = (self.external_ip, self.port)
        self.server.bind(server_address)

        sock.listen(1)

        while True:

            self.connection, client_address = sock.accept()

            try:
                #  recieve the passcode
                while True:
                    data = self.connection.recv()

                    if data == self.passcode:

                        self.connection.sendall(self.file)

                    else:
                        raise IncorrectPasscode("Server recieved a connection which passed an incorrect passcode")

            except:
                raise FailedToPost("Communications with the client failed")

            finally:
                #  end the connection
                connection.close()


    def seek(self):

        #  seek a specific IP [+port] for server

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = (self.external_ip, self.port)
        self.client.connect(server_address)

        self.file = []

        try:
            if self.passcode:
                self.client.sendall(self.passcode)

            while True:
                data = sock.recv()

                if data:
                    self.file.append(data)
                else:
                    break
            else:
                if self.path:
                    with open(path, "w") as file:
                        file.write(self.file)
                else:
                    print(self.file)

        except:
            raise FailedToSeek("Communications with server failed")

        finally:
            self.client.close()
