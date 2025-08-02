import socket


# Cấu hình
HOST = '0.0.0.0'  # Lắng nghe trên tất cả các giao diện mạng
PORT = 12346       # Cổng giao tiếp


# Tạo socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))  # Gắn socket vào địa chỉ và cổng
    print(f"Listening for broadcast messages on port {PORT}...")

    while True:
        data, addr = s.recvfrom(1024)  # Giới hạn kích thước gói tin
        print(f"Received: {data.decode()} from {addr}")
root@raspberrypi4-64:/home/root# cat receive_uni_v6.py
import socket

PORT = 5007

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Cho phép dùng lại cổng
sock.bind(('', PORT))

print(f"Lang nghe Unicast IPv6 trêncong {PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    print(f"Unicast từ {addr}: {data.decode()}")