from http.server import BaseHTTPRequestHandler
from urllib import parse

from marvel_service import service_functions

# import route
# import json


class MethodHandler(BaseHTTPRequestHandler):
    """MethodHandler - class which describes handling REST API methods

       do_GET - reaction on method GET, reads information about entity
       do_POST - create new entity at the point
       do_DELETE -  delete entity from point
       do_PATCH  - update entity

       URI: /end_point/:entity/?:options

    """

    # Didn't find a way how to do it correct
    # todo - redesign if any good solution will be founded
    # controller -  class attribute will be created when object created,
    # attribute configured with custom edited service_functions.urlmapping
    # controller - contains mapping for endpoints and custom functions
    controller = service_functions.MethodsCallDispatcher()
    controller.route_config(service_functions.urlmapping)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset = utf-8')
        self.end_headers()

    def do_GET(self):
        """Method GET"""

        parsed_path = parse.urlparse(self.path)
        # print(parsed_path)
        # /endpoint/entity/?:params
        # /hero/loky
        # TODO issue with sending header
        answer = self.controller.on_get(parsed_path)

        # Make Answer
        self._set_headers()
        self.send_response(answer['error_code'])
        if answer['status']:
            self.send_header('Content-Type', 'application/json; charset=utf-8')
        else:
            self.send_header('Content-Type', 'plain/text; charset=utf-8')

        self.end_headers()
        self.wfile.write(answer['message'].encode('utf-8'))

    def do_DELETE(self):
        """Method DELETE"""
        parsed_path = parse.urlparse(self.path)
        # /endpoint/entity
        # /hero/loky

        answer = self.controller.on_delete(parsed_path)

        # Make Answer
        self._set_headers()
        self.send_response(answer['error_code'])
        if answer['status']:
            self.send_header('Content-Type', 'application/json; charset=utf-8')
        else:
            self.send_header('Content-Type', 'plain/text; charset=utf-8')

        self.end_headers()
        self.wfile.write(answer['message'].encode('utf-8'))

    def do_PATCH(self):
        """Method UPDATE"""

        parsed_path = parse.urlparse(self.path)
        # /endpoint/entity
        # /hero/loky
        patch_body = self.rfile.read(int(self.headers['Content-Length']))
        print(patch_body)
        answer = self.controller.on_patch(parsed_path, patch_body)

        # Make Answer
        self._set_headers()
        self.send_response(answer['error_code'])
        if answer['status']:
            self.send_header('Content-Type', 'application/json; charset=utf-8')
        else:
            self.send_header('Content-Type', 'plain/text; charset=utf-8')

        self.end_headers()
        self.wfile.write(answer['message'].encode('utf-8'))

    def do_POST(self):
        """Method POST"""

        parsed_path = parse.urlparse(self.path)
        # get body
        post_body = self.rfile.read(int(self.headers['Content-Length']))

        answer = self.controller.on_post(parsed_path, post_body)

        # Make Answer
        self._set_headers()
        self.send_response(answer['error_code'])
        if answer['status']:
            self.send_header('Content-Type', 'application/json; charset=utf-8')
        else:
            self.send_header('Content-Type', 'plain/text; charset=utf-8')

        self.end_headers()
        self.wfile.write(answer['message'].encode('utf-8'))


def run_service(port: int = 8080):
    from http.server import HTTPServer
    server = HTTPServer(('localhost', port), MethodHandler)
    print('🚀: Starting server...')
    print('😅: Server started.')
    print('👀: use <Ctrl-C> to stop')

    print(f"\n\nUse: http://localhost:{port}/heroes to start work with server")
    print(f"\nYou can start from command:\n  curl -X GET  "
          f"http://localhost:{port}/heroes")
    server.serve_forever()


if __name__ == '__main__':
    run_service()
