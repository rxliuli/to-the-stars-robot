from llama_index import (
    GPTSimpleVectorIndex,
    SimpleDirectoryReader,
)
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os
os.environ["OPENAI_API_KEY"] = os.environ.get('OPENAI_API_KEY')


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
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        if 'q' in query_params:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            r = str(query(query_params['q'][0]))
            print("r", r)
            self.wfile.write(r.encode())
            # self.wfile.write(str('hello world').encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing 'q' parameter")


PORT = int(os.environ.get('PORT'))

with HTTPServer(("", PORT), MyHandler) as httpd:
    print("env: ", os.environ.get(
        'OPENAI_API_KEY'), PORT)
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
