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
client_port = int(client_port)

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

neighbor_conn = None

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SOREUSEADDR, 1)
server_sock.bind((server_ip, server_port))
server_sock.listen(5)

def accept_connection():
    neighbor_conn, addr = server_sock.accept()
    print("neighbor connected to server")

threading.Thread(target=accept_connection).start()

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        client_sock.connect((client_ip, client_port))
        print("client connected to next node")
        break
    except:
        time.sleep(5)

while neighbor_conn is None:
    time.sleep(5)