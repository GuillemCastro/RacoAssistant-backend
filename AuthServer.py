import http.server as HttpServer
from urllib.parse import urlparse, parse_qs
import FIB
from threading import Thread
from BotConfig import BotConfig

class AuthServer(HttpServer.HTTPServer, object):

    def __init__(self, server_address, RequestHandlerClass, authQueue):
        super(AuthServer, self).__init__(server_address=server_address, RequestHandlerClass=RequestHandlerClass)
        self.authQueue = authQueue

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
            if 'code' in params:
                self.send_response(200)
                self.end_headers()
                user_id = params['state'][0]
                code = params['code'][0]
                thread = Thread(target=process_auth_code, args=(user_id, code))
                thread.start()
                self.wfile.write("OK 200".encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write("REQUEST ERROR 400".encode("utf-8"))
        else:
            self.send_response(401)
            self.end_headers()
            self.wfile.write("UNAUTHORIZED 401".encode("utf-8"))



def process_auth_code(user_id, auth_code):
    token = FIB.get_access_token(BotConfig.client_id, BotConfig.client_secret, BotConfig.complete_host, user_id, auth_code)
    if token:
        user = FIB.get_name(token)
        print("Welcome " + user.name.capitalize() + " " + user.surname.capitalize())
        #Save it to DB
    else:
        raise RuntimeError()
