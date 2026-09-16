import json
import socket
import threading
import time
import uuid

id = uuid.uuid4()

print("uuid", id)

file = open("pa2/config.txt")
lines = file.read()
file.close()

lines = lines.split('\n')

server_ip, server_port = lines[0].split(',')
client_ip, client_port = lines[1].split(',')

server_port = int(server_port)
lient_port = int(client_port)

print("server", server_ip, server_port)
print("client", client_ip, client_port)

class Message:
    def __init__(self, uuid, flag=0):
        self.uuid = uuid
        self.flag = flag
    
    def json(self):
        return json.dumps({
            "uuid": str(self.uuid),
            "flag": self.flag
        })