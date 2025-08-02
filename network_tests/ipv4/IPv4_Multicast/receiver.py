import socket
import struct
import json
import threading
import time
from datetime import datetime

class MulticastReceiver:
    def __init__(self, multicast_group='224.1.1.1', port=5007, interface='0.0.0.0'):
        """
        Khởi tạo Multicast Receiver

        Args:
            multicast_group (str): Địa chỉ IP multicast group
            port (int): Cổng để nhận dữ liệu
            interface (str): Interface để bind (0.0.0.0 = tất cả interfaces)
        """
        self.multicast_group = multicast_group
        self.port = port
        self.interface = interface
        self.sock = None
        self.running = False
        self.message_count = 0
        self.start_time = None

    def setup_socket(self):
        """Thiết lập socket multicast và tham gia nhóm multicast"""
        try:
            # Tạo UDP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Cho phép reuse address
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind socket đến port
            self.sock.bind(('', self.port))

            # Tạo multicast request để tham gia nhóm
            # struct.pack: 4s = 4 bytes cho IP multicast, 4s = 4 bytes cho local interface
            mreq = struct.pack('4s4s',
                             socket.inet_aton(self.multicast_group),
                             socket.inet_aton(self.interface))

            # Tham gia multicast group (gửi IGMP JOIN message)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            # Thiết lập timeout để có thể interrupt
            self.sock.settimeout(1.0)

            print(f"✓ Socket multicast receiver đã được thiết lập")
            print(f"  - Multicast Group: {self.multicast_group}")
            print(f"  - Port: {self.port}")
            print(f"  - Interface: {self.interface}")
            print(f"  - Đã tham gia nhóm multicast (IGMP JOIN)")

        except Exception as e:
            print(f"✗ Lỗi khi thiết lập socket: {e}")
            raise

    def leave_multicast_group(self):
        """Rời khỏi nhóm multicast (gửi IGMP LEAVE message)"""
        if self.sock:
            try:
                mreq = struct.pack('4s4s',
                                 socket.inet_aton(self.multicast_group),
                                 socket.inet_aton(self.interface))

                # Rời khỏi multicast group
                self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
                print(f"📤 Đã rời khỏi nhóm multicast (IGMP LEAVE)")

            except Exception as e:
                print(f"⚠️ Lỗi khi rời nhóm multicast: {e}")

    def receive_messages(self):
        """Nhận thông điệp multicast"""
        if not self.sock:
            raise RuntimeError("Socket chưa được thiết lập. Gọi setup_socket() trước.")

        self.running = True
        self.start_time = time.time()

        print(f"🔄 Bắt đầu nhận thông điệp multicast...")
        print("Nhấn Ctrl+C để dừng...\n")

        try:
            while self.running:
                try:
                    # Nhận dữ liệu
                    data, addr = self.sock.recvfrom(1024)

                    # Xử lý thông điệp nhận được
                    self.process_message(data, addr)

                except socket.timeout:
                    # Timeout - tiếp tục loop
                    continue
                except Exception as e:
                    if self.running:
                        print(f"⚠️ Lỗi khi nhận dữ liệu: {e}")

        except KeyboardInterrupt:
            print("\n🛑 Dừng nhận thông điệp")
        finally:
            self.running = False
            self.print_statistics()

    def process_message(self, data, addr):
        """
        Xử lý thông điệp nhận được

        Args:
            data (bytes): Dữ liệu nhận được
            addr (tuple): Địa chỉ của sender
        """
        try:
            # Decode và parse JSON
            message_str = data.decode('utf-8')
            message_data = json.loads(message_str)

            self.message_count += 1

            # Hiển thị thông tin thông điệp
            print(f"📨 Thông điệp #{self.message_count}")
            print(f"   👤 Từ: {addr[0]}:{addr[1]}")
            print(f"   ⏰ Thời gian: {message_data.get('timestamp', 'N/A')}")
            print(f"   📝 Nội dung: {message_data.get('message', 'N/A')}")
            print(f"   🏷️ Người gửi: {message_data.get('sender', 'Unknown')}")
            print(f"   📏 Kích thước: {len(data)} bytes")
            print("-" * 50)

        except json.JSONDecodeError:
            # Nếu không phải JSON, hiển thị raw data
            self.message_count += 1
            print(f"📨 Thông điệp thô #{self.message_count}")
            print(f"   👤 Từ: {addr[0]}:{addr[1]}")
            print(f"   📝 Nội dung: {data.decode('utf-8', errors='ignore')}")
            print(f"   📏 Kích thước: {len(data)} bytes")
            print("-" * 50)

        except Exception as e:
            print(f"⚠️ Lỗi khi xử lý thông điệp: {e}")

    def print_statistics(self):
        """In thống kê"""
        if self.start_time:
            duration = time.time() - self.start_time
            print(f"\n📊 THỐNG KÊ:")
            print(f"   📨 Tổng thông điệp nhận: {self.message_count}")
            print(f"   ⏱️ Thời gian chạy: {duration:.2f} giây")
            if duration > 0:
                print(f"   📈 Tốc độ trung bình: {self.message_count/duration:.2f} msg/s")

    def monitor_mode(self):
        """Chế độ monitor - chỉ hiển thị thông tin cơ bản"""
        if not self.sock:
            raise RuntimeError("Socket chưa được thiết lập. Gọi setup_socket() trước.")

        self.running = True
        self.start_time = time.time()

        print(f"🔍 Chế độ monitor - chỉ hiển thị thông tin cơ bản")
        print("Nhấn Ctrl+C để dừng...\n")

        try:
            while self.running:
                try:
                    data, addr = self.sock.recvfrom(1024)
                    self.message_count += 1

                    # Hiển thị thông tin ngắn gọn
                    current_time = datetime.now().strftime('%H:%M:%S')
                    print(f"[{current_time}] #{self.message_count} từ {addr[0]} ({len(data)} bytes)")

                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"⚠️ Lỗi: {e}")

        except KeyboardInterrupt:
            print("\n🛑 Dừng monitor")
        finally:
            self.running = False
            self.print_statistics()

    def close(self):
        """Đóng socket"""
        if self.sock:
            self.leave_multicast_group()
            self.sock.close()
            print("🔒 Socket đã được đóng")

def main():
    """Hàm chính"""
    print("=" * 60)
    print("📡 IPv4 MULTICAST RECEIVER")
    print("=" * 60)

    # Cấu hình mặc định
    MULTICAST_GROUP = '224.12.1.1'
    PORT = 5007
    INTERFACE = '0.0.0.0'

    # Tạo receiver
    receiver = MulticastReceiver(MULTICAST_GROUP, PORT, INTERFACE)

    try:
        # Thiết lập socket
        receiver.setup_socket()

        # Menu lựa chọn
        print("\n📋 MENU LỰA CHỌN:")
        print("1. Nhận thông điệp chi tiết")
        print("2. Chế độ monitor (thông tin cơ bản)")

        choice = input("\nChọn chế độ (1-2): ").strip()

        if choice == '1':
            receiver.receive_messages()
        elif choice == '2':
            receiver.monitor_mode()
        else:
            print("❌ Lựa chọn không hợp lệ")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        receiver.close()

if __name__ == "__main__":
    main()