FROM python:3.11.4-slim-bullseye
RUN apt-get update
RUN apt-get -y install git
RUN git clone https://github.com/StrajnarFilip/websocket-relay
WORKDIR /websocket-relay
RUN pip install .
ENTRYPOINT [ "uvicorn" ,"--host", "0.0.0.0", "--port", "5000", "websocket_relay:relay" ]