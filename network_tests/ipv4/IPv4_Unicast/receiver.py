import socket

PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))

print(f"Lang nghe Unicast Ipv4 tren cong {PORT}...")
while True:
    data, addr = sock.recvfrom(1024)
    print(f"Unicast từ {addr}: {data.decode()}")