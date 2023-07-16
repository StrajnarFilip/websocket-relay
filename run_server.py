from subprocess import run
from sys import executable

run([executable, "-m", "pip", "install", "."])
run([
    "uvicorn", "--host", "0.0.0.0", "--port", "5000", "websocket_relay:relay"
])
