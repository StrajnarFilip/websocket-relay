import uvicorn

if __name__ == "__main__":
    uvicorn.run("websocket_relay:relay", port=5000, log_level="info")