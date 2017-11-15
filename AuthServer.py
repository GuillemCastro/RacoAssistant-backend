import http.server as HttpServer
from urllib.parse import urlparse, parse_qs
import FIB
from threading import Thread
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
client_id = config['FIB']['ClientID']
client_secret = config['FIB']['ClientSecret']


class AuthServer(HttpServer.HTTPServer, object):

    def __init__(self, server_address, RequestHandlerClass, authQueue):
        super(AuthServer, self).__init__(server_address=server_address, RequestHandlerClass=RequestHandlerClass)
        self.authQueue = authQueue
        print("__INIT__")


class AuthRequestHandler(HttpServer.BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        super(AuthRequestHandler, self).__init__(request=request, client_address=client_address, server=server)

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        path = urlparse(self.path).path
        if path == "/":
            if 'user_id' in params:
                self.send_response(200)
                self.end_headers()
                print("GET")
                if 'error' in params:
                    return #Send error message to user
                user_id = params['user_id']
                auth_code = params['code'][0]
                th = Thread(target=process_auth_code, args=(user_id, auth_code))
                th.start()
                self.wfile.write("OK".encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write("REQUEST ERROR".encode("utf-8"))
        else:
            self.send_response(401)
            self.end_headers()
            self.wfile.write("UNAUTHORIZED".encode("utf-8"))



def process_auth_code(user_id, auth_code):
    print("client_id: " + client_id)
    print(" client_secret: " + client_secret)
    print(" auth_code: " + auth_code)
    token = FIB.auth_code_to_access_token(client_id, client_secret, '127.0.0.1', auth_code, user_id)
    print ("token" + token.token)
    # Save token to DB
