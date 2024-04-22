import socket
import threading
import os
import ast
from random import randint
from time import sleep

# Setting up the host, ports and buffersize
host = "localhost"
sender = 9876
sender_tcp = 9877
receiver = 8080
receiver_tcp = 8081
buffersize = 2048
sequence = 0
event = threading.Event()

peer = (host, receiver)
peer_tcp = (host, receiver_tcp)

# Creating socket for receiving messages using UDP
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock.bind((host, sender))
# Creating sockets for sending and receiving files using TCP
file_send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
file_recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
file_recv_sock.bind((host, sender_tcp))

# Clearing the terminal screen
if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

print("========== Chat ==========")
print('Type "exit" to exit chat')
print("Type $SEND <file-path> to send file")

# Function to handle sending files
def send_file(path: str):
    file_send_sock.connect(peer_tcp)
    file = open(path, "rb")
    file_type = path.split(".")[-1]
    file_send_sock.send(file_type.encode())
    file_send_sock.sendall(file.read())
    file_send_sock.send(b"<END>")
    file.close()
    file_send_sock.close()
    print("Enter a new message: ")

# Function to handle receiving files over TCP
def tcp_recv():
    while True:
        client, _ = file_recv_sock.accept()
        file_type = client.recv(1024).decode()
        file_name = f"received-{randint(0, 100)}.{file_type}"
        file = open(file_name, "wb")
        while True:
            file_bytes = client.recv(1024)
            if file_bytes[-5:] == b"<END>":
                file.write(file_bytes[:-5])
                break
            else:
                file.write(file_bytes)
        file.close()
        client.close()
        print(f"File {file_name} received")
        print("\nEnter a new message: ")

# Function to handle incoming messages
def handle_receives():
    global sequence
    old_msg = ""
    old_Seq = 421  # Random starting number for old sequence
    while True:
        rec_array=[]
        send_array=[]
        message=[]
        try:
            message, _ = recv_sock.recvfrom(buffersize)
            message = message.decode()
            msg = message
            rec_array = ast.literal_eval(message)

            if rec_array[0] == "ACK" and rec_array[1] == sequence - 1:
                if old_Seq != sequence - 1:
                    print("Peer Acked the message")
                    print("\nEnter a new message: ")
                    old_Seq = sequence - 1
                    event.set()
            elif msg == old_msg:
                print("\nFound a duplicate, resending ACK")
                print("\nEnter a new message:")
                send_array.append("ACK")
                send_array.append(rec_array[1])
                recv_sock.sendto(str(send_array).encode(), peer)
            elif msg !="":
                ready_msg = msg.split(",")
                print("\nPeer: {}".format(ready_msg[0][1:]))
                print("\nEnter a new message:")
                send_array.append("ACK")
                send_array.append(rec_array[1])
                recv_sock.sendto(str(send_array).encode(), peer)
                old_msg = msg
        except:
            pass

# Function to handle sending messages
def handle_sends():
    global sequence
    my_array = []
    print("Enter a new message: ")
    while True:
        my_array = []
        message = input("")
        print("")
        if message == "exit":
            os._exit(0)
        elif message[:5] == "$SEND":
            send_statement = message.split(" ", 1)
            send_file(send_statement[1])
        else:
            my_array.append(message)
            my_array.append(sequence)
            recv_sock.sendto(str(my_array).encode(), peer)
            sequence += 1
            while not event.wait(timeout=1):
                print("Time Exceeded, resending")
                recv_sock.sendto(str(my_array).encode(), peer)

# Function to handle file receiving thread
def handle_file():
    while True:
        file_recv_sock.listen()
        tcp_recv()

# Creating threads for handling send, receives and file receive
t1 = threading.Thread(target=handle_sends)
t2 = threading.Thread(target=handle_receives)
t3 = threading.Thread(target=handle_file)

t1.start()
t2.start()
t3.start()
