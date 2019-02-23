#!/usr/bin/env python3

# Custom, minimal-ish HTTP(S) file upload endpoint
# Setup: 
#        apt install -y python3 python3-pip
#        pip3 install multipart argparse ssl
#        mkdir -p /var/www/html/uploads
#        ./this.py --setup-ssl

# WARNING: The odds of this being secure are very low. Use at your own risk.

from http.server import HTTPServer, SimpleHTTPRequestHandler
import multipart
import ssl
from io import BytesIO

import shutil
import os
import time

import argparse



parser=argparse.ArgumentParser(description='An HTTP(S) upload endpoint for APK files. Starts the analysis process.')
parser.add_argument('-p',"--port", default=80, type=int, required=False, help="The port to listen on")
parser.add_argument('-a',"--address", default="0.0.0.0", required=False, help="The address to listen on")
parser.add_argument('-k',"--keyfile", default="key.pem", required=False, help="The path to the SSL key file")
parser.add_argument('-c',"--certfile", default="cert.pem", required=False, help="The path to the SSL certificate file")
parser.add_argument('-s',"--ssl", required=False, action="store_true", help="Enable SSL mode")
parser.add_argument("--setup-ssl", required=False, action="store_true", help="Generate SSL certificate and key, then exit")
parser.add_argument("--upload-dir", required=False, default="/var/www/html/uploads/", help="The directory to upload things to. Default: /var/www/html/uploads")
parser.add_argument("--serve-dir", required=False, default="/var/www/html/", help="The directory to upload things to. Default: /var/www/html/")
parser.add_argument("--no-serve", required=False, action="store_true", help="Do not serve files, only accept uploads")



args = parser.parse_args()

args.upload_dir=os.path.realpath(os.path.join(os.path.expanduser(args.upload_dir)))
args.serve_dir=os.path.realpath(os.path.join(os.path.expanduser(args.serve_dir)))


######################################################
#   Accept submissions of APK files to be analyzed
#
#   Example upload using curl:
#   curl -k -F 'name_of_upload=@/path/to/local/file' https://127.0.0.1/
######################################################
class UploadServer(SimpleHTTPRequestHandler):
    def _reply(self, msg):
        self.send_response(200)
        self.send_header('Content-Length', len(msg))
        self.end_headers()
        self.wfile.write(msg)
        
    def do_404(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"""
<html>
<head><title>404 Not Found</title></head>
<body bgcolor="white">
<center><h1>404 Not Found</h1></center>
<hr><center>nginx/1.10.3 (Ubuntu)</center>
</body>
</html>
"""
)
    def serve(self, path):
        try:
            print("\tMapping request for {} to {}".format(self.path, path))
            content_len = os.stat(path).st_size
            f = open(path, 'rb')
            self.send_response(200)
            self.send_header('Content-Length', content_len)
            self.end_headers()
            print("Serving {} to {}".format(self.path, self.client_address[0]))
            shutil.copyfileobj(f, self.wfile)
            f.close()
        except Exception as e:
            print("{} Error serving Path: {}. {}".format(self.client_address[0], path, e))
            self.do_404()

    def do_GET(self):
        if args.no_serve:
            msg = """
Upload a file using:
curl -k -F'name_of_upload@/path/to/local/file' http[s]://X.X.X.X:{}/
""".format(args.port).encode()
            self._reply(msg)
        else:
            rel_path = os.path.normpath("./{}".format(self.path))
            filepath=os.path.join(args.serve_dir, rel_path)
            assert os.path.realpath(filepath).startswith(os.path.realpath(args.serve_dir)), "SECURITY VIOLATION: directory traversal detected!"
            if os.path.isdir(filepath):
                print("Listing directory: {}".format(filepath))
                dir_list = self.list_directory(filepath)
                if dir_list:
                    shutil.copyfileobj(dir_list, self.wfile)
            else:
                self.serve(filepath)

    def do_POST(self):
        host = self.client_address[0]
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            stream = BytesIO(body)
            boundary = stream.readline()
            boundary = boundary.strip(b"\r\n")[2:]
            stream.seek(0)
            parser = multipart.MultipartParser(stream, boundary)
             
            for part in parser:
                # Try not to allow uploads to things outside of upload_dir.
                # WARNING: probably not secure
                localpath = os.path.join(args.upload_dir, os.path.basename(os.path.realpath(part.name)))
                print("Submission {} uploading to {}".format(part.name, localpath))
                with open(localpath, 'wb') as f:
                    shutil.copyfileobj(part.file, f)
                
        except Exception as e:
            print(e)
            self._reply(str(e).encode())
        else:
            self._reply(b"Upload successful!\n")

    # Stop log messages from printing to the screen
    #def log_message(self, format, *args):
    #    return

def main():
    if args.setup_ssl:
        os.system('openssl req -nodes -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365')
        print("key.pem and cert.pem created")
        return

    httpd = HTTPServer((args.address, args.port), UploadServer)
    if args.ssl:
        httpd.socket = ssl.wrap_socket (httpd.socket, 
                   keyfile=args.keyfile, 
                   certfile=args.certfile, server_side=True)
    
    httpd.serve_forever()

if __name__=="__main__":
    main()

