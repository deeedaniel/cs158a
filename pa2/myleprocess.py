import json
import socket
import threading
import time
import uuid

def write_log(text):
    with open("log.txt", "a") as file:
        file.write(text)
        file.write("\n")
    print(text)

id = uuid.uuid4()

# print("uuid", id)
write_log("process started, id:", id)

file = open("pa2/config.txt")
lines = file.read()
file.close()

lines = lines.split('\n')

server_ip, server_port = lines[0].split(',')
client_ip, client_port = lines[1].split(',')

server_port = int(server_port)
client_port = int(client_port)

# print("server", server_ip, server_port)
# print("client", client_ip, client_port)

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
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind((server_ip, server_port))
server_sock.listen(5)

def accept_connection():
    global neighbor_conn
    neighbor_conn, addr = server_sock.accept()
    # print("neighbor connected to server")

threading.Thread(target=accept_connection).start()

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        client_sock.connect((client_ip, client_port))
        # print("client connected to next node")
        break
    except:
        time.sleep(5)

while neighbor_conn is None:
    time.sleep(5)

# print("ring formed")

msg = Message(id)
msg_json = msg.json()

client_sock.sendall(msg_json.encode())
# print("sent message")
write_log(f"Sent message. UUID={id}. Flag=0")

leader_id = None
state = 0

while True:
    data = neighbor_conn.recv(1024)

    if not data:
        break

    data_decoded = json.loads(data.decode())
    data_uuid = data_decoded["uuid"]
    data_flag = data_decoded["flag"]

    if data_flag == 1:
        leader_id = data_uuid

        if leader_id != str(id):
            client_sock.sendall(data)

        break

    else:
        if data_uuid > str(id):
            client_sock.sendall(data)
        
        elif data_uuid == str(id):
            leader_id = str(id)
            win_msg = Message(id, flag=1)
            client_sock.sendall(win_msg.json().encode())
            break

        else:
            pass

# print("The leader is ", leader_id)