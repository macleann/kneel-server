import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_metals, get_single_metal, create_metal, delete_metal, update_metal, get_all_styles, get_single_style, create_style, delete_style, update_style, get_all_sizes, get_single_size, create_size, delete_size, update_size, get_all_orders, get_single_order, create_order, delete_order


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def do_GET(self):
        """Handles GET requests to the server """
        self._set_headers(200)
        response = {}

        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            if id is not None:
                response = get_single_metal(id)
                if response is None:
                    self._set_headers(404)
                    response = {
                        "message": "That metal is not currently in stock for jewelry."}
            else:
                response = get_all_metals()

        elif resource == "styles":
            if id is not None:
                response = get_single_style(id)
                if response is None:
                    self._set_headers(404)
                    response = {
                        "message": "That style is not currently offered for jewelry."}
            else:
                response = get_all_styles()

        elif resource == "sizes":
            if id is not None:
                response = get_single_size(id)
                if response is None:
                    self._set_headers(404)
                    response = {
                        "message": "That size is not currently available for jewelry."}
            else:
                response = get_all_sizes()

        elif resource == "orders":
            if id is not None:
                response = get_single_order(id)
                if response is None:
                    self._set_headers(404)
                    response = {
                        "message": "That order was never placed, or was cancelled."}
            else:
                response = get_all_orders()

        else:
            response = []

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server """
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        new_resource = None

        check_keys = {
            "metals": ["metal", "price"],
            "styles": ["style", "price"],
            "sizes": ["carets", "price"],
            "orders": ["metalId", "sizeId", "styleId", "timestamp"]
        }

        if resource == "metals":
            if [key for key in check_keys["metals"] if key in post_body] == check_keys["metals"]:
                new_resource = create_metal(post_body)
            else:
                self._set_headers(400)
                error_keys = [key for key in check_keys["metals"]
                              if key not in post_body]
                if len(error_keys) > 1:
                    new_resource = f"message: {' and '.join(error_keys)} are required"
                else:
                    new_resource = f"message: {error_keys[0]} is required"
        elif resource == "styles":
            if [key for key in check_keys["styles"] if key in post_body] == check_keys["styles"]:
                new_resource = create_style(post_body)
            else:
                self._set_headers(400)
                error_keys = [key for key in check_keys["styles"]
                              if key not in post_body]
                if len(error_keys) > 1:
                    new_resource = f"message: {' and '.join(error_keys)} are required"
                else:
                    new_resource = f"message: {error_keys[0]} is required"
        elif resource == "sizes":
            if [key for key in check_keys["sizes"] if key in post_body] == check_keys["sizes"]:
                new_resource = create_size(post_body)
            else:
                self._set_headers(400)
                error_keys = [key for key in check_keys["sizes"]
                              if key not in post_body]
                if len(error_keys) > 1:
                    new_resource = f"message: {' and '.join(error_keys)} are required"
                else:
                    new_resource = f"message: {error_keys[0]} is required"
        elif resource == "orders":
            if [key for key in check_keys["orders"] if key in post_body] == check_keys["orders"]:
                new_resource = create_order(post_body)
            else:
                self._set_headers(400)
                error_keys = [key for key in check_keys["orders"]
                              if key not in post_body]
                if len(error_keys) > 2:
                    new_resource = f"message: {', '.join(error_keys)} are required"
                elif len(error_keys) > 1:
                    new_resource = f"message: {' and '.join(error_keys)} are required"
                else:
                    new_resource = f"message: {error_keys[0]} is required"

        self.wfile.write(json.dumps(new_resource).encode())

    def do_PUT(self):
        """Handles PUT requests to the server """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            self._set_headers(204)
            update_metal(id, post_body)
        elif resource == "styles":
            self._set_headers(204)
            update_style(id, post_body)
        elif resource == "sizes":
            self._set_headers(204)
            update_size(id, post_body)
        elif resource == "orders":
            self._set_headers(405)
            response = {
                "message": "Cannot update an order once it has been placed."}
            self.wfile.write(json.dumps(response).encode())

        self.wfile.write("".encode())

    def do_DELETE(self):
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            delete_metal(id)
        elif resource == "styles":
            delete_style(id)
        elif resource == "sizes":
            delete_size(id)
        elif resource == "orders":
            delete_order(id)

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
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        try:
            id = int(path_params[2])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id)

# point of this application.


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
