import json
import socket
import threading
import time
import uuid

uuid = uuid.uuid4()

print("uuid", uuid)

file = open("pa2/config.txt")
lines = file.read()
file.close()

lines = lines.split('\n')

server_ip, server_port = lines[0].split(',')
client_ip, client_port = lines[1].split(',')

print(server_ip, server_port)
print(client_ip, client_port)