import socket
import time

# Cấu hình
DEST_IP = "fd53:1234:5678:5::39"  # Thay bằng địa chỉ IPv6 thực của máy nhận
PORT = 10000

def create_sender():
    """Tạo socket gửi IPv6 unicast"""
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    return sock

def send_messages():
    """Gửi thông điệp IPv6 unicast"""
    sock = create_sender()

    print(f"Gửi IPv6 unicast đến [{DEST_IP}]:{PORT}")
    print("Ctrl+C để dừng\n")

    counter = 0
    try:
        while True:
            counter += 1
            message = f"Unicast IPv6 #{counter} - {time.strftime('%H:%M:%S')}"
            try:
                sock.sendto(message.encode('utf-8'), (DEST_IP, PORT))
                print(f"Gửi: {message}")
            except socket.gaierror as e:
                print(f"Lỗi khi gửi: {e}")
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nĐã dừng gửi")
    finally:
        sock.close()

if __name__ == "__main__":
    send_messages()