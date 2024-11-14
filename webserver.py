# Ref:
#    - https://dev.to/gavi/custom-mime-type-with-python-3-httpserver-530l
#    - https://trycatchdebug.net/news/1147876/serving-specific-mime-types-with-python-s-http-server

import http.server
import os
import sass

from urllib.parse import urlparse


custom_mime_types = {
    ".scss": "text/scss",
    # Add more custom MIME types here as needed
}

class ExtendedHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def _read_file(self, path):
        """Read the file at 'path' and return its content, byte-encoded.

        If 'path' points to a non-existing css file, try reading the matching
        scss file and processing it.

        IOError is raised upon failure.
        """

        try:
            with open(path, 'rb') as file:
                data = file.read()
        except IOError as e:
            basename, extension = os.path.splitext(path)

            # If a css file was requested, try to see if a corresponding scss
            # file exists
            if extension == '.css':
                scss_path = basename + '.scss'
                print(f'{path} not found, trying {scss_path}')
                try:
                    css_data = sass.compile(filename=scss_path)
                    data = css_data.encode()
                except sass.CompileError as e:
                    print(f'.scss compilation error: {e}')
                    raise IOError
            else:
                raise e

        return data

    def do_GET(self):
        """Serve a GET request."""

        # Handle index URLs
        if self.path.endswith('/'):
            self.path += 'index.html'

        # Process the request
        try:
            # Prepare the response header
            self.send_response(200)
            mimetype = self.guess_type(self.path)
            self.send_header("Content-type", mimetype)
            self.end_headers()

            # Handle the payload
            fs_path = self.path.removeprefix('/')
            data = self._read_file(fs_path)
            self.wfile.write(data)
        except IOError:
            self.send_error(404, "File not found")

    def guess_type(self, path):
        """Extend the superclass' method with additional MIME types."""

        # Check if path's file extension has a custom MIME type
        parsed_url = urlparse(path)
        _, extension = os.path.splitext(parsed_url.path)
        if extension in custom_mime_types:
            return custom_mime_types[extension]

        # Otherwise, fallback to the default MIME type guessing
        return super().guess_type(path)

if __name__ == '__main__':
    server_address = ('', 8000)
    server = http.server.HTTPServer(server_address, ExtendedHTTPRequestHandler)
    print(f'Serving on port {server_address[1]}...')
    server.serve_forever()
