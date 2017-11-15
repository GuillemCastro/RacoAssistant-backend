from urllib import request, parse, error
import json
from datetime import datetime

AUTH_URL = "https://api.fib.upc.edu/v2/o/authorize"
TOKEN_URL = "https://api.fib.upc.edu/v2/o/token"


def get_auth_url(client_id, host_uri, user_id):
    redirect_url = host_uri + '?' + parse.urlencode({'user_id': user_id})
    params = parse.urlencode({'redirect_uri': redirect_url, 'client_id': client_id,
                              'response_type': 'code', 'scope': 'read', 'state': 'random_state_string',
                              'approval_prompt': 'auto'}, doseq=True)
    return AUTH_URL + '?' + params


def auth_code_to_access_token(client_id, client_secret, redirect_uri, auth_code, user_id):
    redirect_url = redirect_uri + '?' + parse.urlencode({'id': user_id})
    data = parse.urlencode({'client_id': client_id, 'client_secret': client_secret, 'redirect_uri': redirect_url,
                            'code': auth_code, 'grant_type': 'authorization_code'}) #.encode("utf-8")
    print("data: " + data)
    try:
        with request.urlopen(TOKEN_URL, data.encode("utf-8")) as f:
            result = f.read()
            return Token.from_json(result)
    except error.HTTPError as e:
        print(e.read())


def refresh_token(token, client_id, client_secret):
    data = parse.urlencode({'grant_type': 'refresh_token', 'refresh_token': token.token, 'client_id': client_id,
                            'client_secret': client_secret})
    with request.urlopen(TOKEN_URL, data) as f:
        result = f.read()
    return Token.from_json(result)


class Token:

    def __init__(self, token, type, expire_date, refresh_token, scope):
        self.token = token
        self.type = type
        self.expire_date = expire_date
        self.refresh_token = refresh_token
        self.scope = scope

    @classmethod
    def from_json(cls, data):
        j_data = json.loads(data)
        expire_data = datetime.today() + j_data['Expires_in']
        return Token(j_data['Access_token'], j_data['Token_type'], expire_data, j_data['Refresh_token'], j_data['Scope'])
