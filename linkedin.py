from rauth.service import OAuth2Service
import httplib2
import webbrowser
from six.moves import BaseHTTPServer
from six.moves import http_client
from six.moves import input
from six.moves import urllib


class ClientRedirectServer(BaseHTTPServer.HTTPServer):
    query_params = {}

class ClientRedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(http_client.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        parts = urllib.parse.urlparse(self.path)
        self.server.query_params = self.__get_query__(parts.query)
        self.wfile.write(
            b'<html><head><title>Authentication Status</title></head>')
        self.wfile.write(
            b'<body><p>The authentication flow has completed.</p>')
        self.wfile.write(b'</body></html>')

    @staticmethod
    def __get_query__(str):
        param_pairs = str.split("&")
        result = []
        for param_pair in param_pairs:
            result.append(param_pair.split("="))
        return dict(result)

    def log_message(self, format, *args):
        """Do not log messages to stdout while running as cmd. line program."""

httpd = ClientRedirectServer(("", 8000), ClientRedirectHandler)

h = httplib2.Http(".cache")
client_id = "86yhtow7c422ui"
client_secret = "dfvwrUMlqjpzeVe2"

linkedin = OAuth2Service(client_id=client_id, client_secret=client_secret, name="linkedin", authorize_url="https://www.linkedin.com/oauth/v2/authorization", access_token_url="https://www.linkedin.com/oauth/v2/accessToken", base_url="https://api.linkedin.com/")

redirect_uri = "http://localhost:8000"
params = { "redirect_uri": redirect_uri, "response_type": "code" }
authorize_url = linkedin.get_authorize_url(**params)
webbrowser.open(authorize_url, new = 1, autoraise=True)
httpd.handle_request()
code = httpd.query_params['code']
data = dict(code=code, redirect_uri=redirect_uri, grant_type="authorization_code")
resp = linkedin.get_raw_access_token(data=data)
access_token = resp.json()["access_token"]

session = linkedin.get_session(access_token)
people = session.get("/v1/people/~?format=json")
