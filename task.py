import subprocess
import sys
import threading
import time
import os

def run():
    def tcp_server():
        subprocess.run(["python", "-m", "speedcompare-server", "tcp"])
    def tcp_client():
        subprocess.run(["python", "-m", "speedcompare", "tcp"])
    
    print("starting server")
    server = threading.Thread(target=tcp_server)
    server.start()
    time.sleep(1)
    print("starting client")
    client = threading.Thread(target=tcp_client)
    client.start()

    server.join()
    client.join()

if not os.environ.get("VIRTUAL_ENV"):
    print("warning: not in virtual environment")
if len(sys.argv) < 2:
    print("no task")
    exit(1)
task_name = sys.argv[1]
tasks = { 'run': run }
if task_name not in tasks:
    print("invalid task")
    exit(1)
tasks[task_name]()
