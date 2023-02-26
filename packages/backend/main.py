
from llama_index import (
    GPTSimpleVectorIndex,
    SimpleDirectoryReader,
)

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


def indexing():
    documents = SimpleDirectoryReader("data").load_data()
    index = GPTSimpleVectorIndex(documents)
    index.save_to_disk("index.json")


def query(s):
    index = GPTSimpleVectorIndex.load_from_disk("index.json")

    response = index.query(s)
    return response


# indexing()
# print(query("Who is Clarisse van Rossum"))

class MyHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin',
                         'http://localhost:8000, https://tts-robot.liuli.moe')
        super().end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        if 'q' in query_params:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(str(query(query_params['q'][0])).encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing 'q' parameter")


PORT = 8000

with HTTPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
