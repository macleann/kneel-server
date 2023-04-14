import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from repository import all, retrieve, create, update

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def do_GET(self):
        """Handles GET requests to the server """
        response = {}
        (resource, id, query_params) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id, query_params)
        self.wfile.write(json.dumps(response).encode())

    def get_all_or_single(self, resource, id, query_params):
        if id is not None:
            response = retrieve(resource, id, query_params)
            
            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ''
        else:
            self._set_headers(200)
            response = all(resource)

        return response

    def do_POST(self):
        """Handles POST requests to the server """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        new_resource = None
        
        if resource == "orders":
            self._set_headers(201)
            new_resource = create(resource, post_body)
        else:
            self._set_headers(400)
            new_resource = f"message: clients are unable to create new {resource}"
                
        self.wfile.write(json.dumps(new_resource).encode())

    def do_PUT(self):
        """Handles PUT requests to the server """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        
        (resource, id) = self.parse_url(self.path)
        
        if resource == "metals":
            self._set_headers(204)
            update(resource, id, post_body)
        else:
            self._set_headers(405)
            response = f"message: clients are unable to update {resource}"
            return self.wfile.write(json.dumps(response).encode())

        self.wfile.write("".encode())
        
    def do_DELETE(self):
        self._set_headers(405)
        self.wfile.write("".encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

        # Replace existing function with this
    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = url_components.query.split("&")
        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id, query_params)

# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
