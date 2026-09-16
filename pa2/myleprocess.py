import json
import socket
import threading
import time
import uuid

# Helper function to write out logs into a file
def write_log(text):
    with open("log.txt", "a") as file:
        file.write(text)
        file.write("\n")
    print(text)

id = uuid.uuid4()

# print("uuid", id)
write_log(f"Process started: uuid={id}")

file = open("config.txt")
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

# Set up server socket to accept incoming TCP connection
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

input("press Eneter when everyone is ready")

# Set up client socket for outgoing connection 
while True:
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((client_ip, client_port))
        # print("client connected to next node")
        break
    except:
        time.sleep(1)

while neighbor_conn is None:
    time.sleep(1)

# print("ring formed")

# Once connection has been made, send initial node's UUID
msg = Message(id)
msg_json = msg.json()

client_sock.sendall(msg_json.encode())
# print("sent message")
write_log(f"Sent: uuid={id}, flag=0")

leader_id = None
state = 0

# Election loop
while True:
    data = neighbor_conn.recv(1024)

    if not data:
        break

    data_decoded = json.loads(data.decode())
    data_uuid = data_decoded["uuid"]
    data_flag = data_decoded["flag"]

    if data_uuid > str(id):
        write_log(f"Received: uuid={data_uuid}, flag={data_flag}, greater, {state}")
    if data_uuid == str(id):
        write_log(f"Received: uuid={data_uuid}, flag={data_flag}, same, {state}")
    if data_uuid < str(id):
        write_log(f"Received: uuid={data_uuid}, flag={data_flag}, less, {state}")

    # Found winner
    if data_flag == 1:
        leader_id = data_uuid

        if leader_id != str(id):
            write_log(f"Sent: uuid={data_uuid}, flag=1")
            client_sock.sendall(data)

        break

    else:
        # Send higher uuid
        if data_uuid > str(id):
            write_log(f"Sent: uuid={data_uuid}, flag=0")
            client_sock.sendall(data)
        
        # Our uuid returned back to us (means highest), send win flag
        elif data_uuid == str(id):
            write_log(f"Sent: uuid={data_uuid}, flag=1")
            leader_id = str(id)
            win_msg = Message(id, flag=1)
            client_sock.sendall(win_msg.json().encode())
            break
        
        # Lower uuid, ignore
        else:
            write_log(f"Message ignored")
            pass

# print("The leader is ", leader_id)
write_log(f"Leader is decided to {leader_id}.")