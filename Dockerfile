FROM python:3.6.14-alpine3.14
WORKDIR /app
RUN cd /app
COPY rpc_server.py .
COPY server.txt .
EXPOSE 3000
#CMD python rpc_server.py
ENTRYPOINT python rpc_server.py
