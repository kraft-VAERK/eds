from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, welcome to the Python server!")
        exit()

def run_server():
    print('Starting server...')
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Server is running on port 5000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()