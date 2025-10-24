#POTANGINA
#Oct 23 2025
#Dasig

import subprocess
import time
import socket
import re

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if is_port_in_use(5006):
    print("Port 5006 is busy, terminating old process...")
    subprocess.run(["bash", "-c", "fuser -k 5006/tcp"])

print("Running setup_db.py ...")
subprocess.run(["python3", "setup_db.py"], check=True)
print("Database setup completed.\n")

print("Starting server...")
server = subprocess.Popen(["python3", "serve.py", "--show"])

time.sleep(5)
url = "http://localhost:5006"
print(f"Opening Microsoft Edge at {url} ...")

# Launch Edge without using PowerShell PassThru PID
subprocess.Popen(["powershell.exe", "-Command", f"Start-Process msedge '{url}'"])

# Wait a bit and get an actual running msedge.exe PID
time.sleep(3)
result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq msedge.exe"], capture_output=True, text=True)
match = re.search(r"msedge\.exe\s+(\d+)", result.stdout)
edge_pid = match.group(1) if match else None

print(f"Monitoring Edge (PID {edge_pid}) — close Edge to stop the server")

try:
    while True:
        time.sleep(5)
        result = subprocess.run(["tasklist", "/FI", f"PID eq {edge_pid}"], capture_output=True, text=True)
        if edge_pid is None or f"{edge_pid}" not in result.stdout:
            print("Edge closed — shutting down server...")
            server.terminate()
            print("Server stopped. Exiting.")
            break

except KeyboardInterrupt:
    print("Interrupted — stopping server...")
    server.terminate()
