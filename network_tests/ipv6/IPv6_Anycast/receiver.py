import socket

ANYCAST_IP = "fd00::100"
PORT = 9999

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.bind((ANYCAST_IP, PORT))

print(f"Listening on {ANYCAST_IP}:{PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    print(f"Received from {addr}: {data}")

~