import socket
import struct
import json
import time
from datetime import datetime

class MulticastReceiverIPv6:
    def __init__(self, multicast_group='ff13::1', port=5007, interface=''):
        """
        Args:
            multicast_group (str): Địa chỉ IPv6 multicast group (ff00::/8)
            port (int): Cổng UDP để nhận dữ liệu
            interface (str): Tên interface mạng (vd: 'eth0'). Để trống = mặc định
        """
        self.multicast_group = multicast_group
        self.port = port
        self.ifname = interface          # lưu tên interface
        self.sock = None
        self.running = False
        self.message_count = 0
        self.start_time = None

    # ---------- Thiết lập & tháo gỡ nhóm ----------
    def setup_socket(self):
        """Tạo socket IPv6, bind và tham gia multicast group"""
        # 1) Tạo socket UDP IPv6
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2) Bind tới '::' (tất cả địa chỉ) + cổng
        self.sock.bind(('::', self.port))

        # 3) Xác định chỉ số interface (ifindex)
        if_index = socket.if_nametoindex(self.ifname) if self.ifname else 0

        # 4) Chuẩn bị request tham gia nhóm
        group_bin = socket.inet_pton(socket.AF_INET6, self.multicast_group)
        mreq = group_bin + struct.pack('@I', if_index)

        # 5) Gửi MLD JOIN
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        # Timeout để có thể Ctrl‑C
        self.sock.settimeout(1.0)

        print("✓ Đã thiết lập socket IPv6 multicast receiver")
        print(f"  - Multicast Group : {self.multicast_group}")
        print(f"  - Port           : {self.port}")
        print(f"  - Interface      : {self.ifname or 'mặc định'}")
        print("  - Đã tham gia nhóm (MLD JOIN)\n")

    def leave_multicast_group(self):
        """Gửi MLD LEAVE và rời nhóm multicast"""
        if not self.sock:
            return
        if_index = socket.if_nametoindex(self.ifname) if self.ifname else 0
        group_bin = socket.inet_pton(socket.AF_INET6, self.multicast_group)
        mreq = group_bin + struct.pack('@I', if_index)
        try:
            self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_LEAVE_GROUP, mreq)
            print("📤 Đã rời nhóm multicast (MLD LEAVE)")
        except Exception as e:
            print(f"⚠️  Lỗi khi rời nhóm: {e}")

    # ---------- Nhận & xử lý ----------
    def _process_message(self, data, addr):
        """Hiển thị thông điệp JSON/Raw"""
        sender_ip = addr[0]          # addr = (ip, port, flowinfo, scopeid)
        try:
            msg = json.loads(data.decode())
            self.message_count += 1
            print(f"📨 Thông điệp #{self.message_count}")
            print(f"   👤 Từ       : {sender_ip}:{addr[1]}")
            print(f"   ⏰ Thời gian: {msg.get('timestamp', 'N/A')}")
            print(f"   📝 Nội dung : {msg.get('message', 'N/A')}")
            print(f"   🏷️  Người gửi: {msg.get('sender', 'Unknown')}")
            print(f"   📏 Kích thước: {len(data)} bytes\n" + "-"*50)
        except json.JSONDecodeError:
            self.message_count += 1
            print(f"📨 RAW #{self.message_count} từ {sender_ip} ({len(data)} bytes)")
            print(data.decode(errors='ignore') + "\n" + "-"*50)

    def receive(self, monitor=False):
        """Nhận multicast: monitor=True -> chỉ log ngắn gọn"""
        if not self.sock:
            raise RuntimeError("Chưa setup socket!")

        self.running = True
        self.start_time = time.time()
        mode = "MONITOR" if monitor else "CHI TIẾT"
        print(f"🔄 Bắt đầu nhận ({mode}) – Ctrl+C để dừng...\n")

        try:
            while self.running:
                try:
                    data, addr = self.sock.recvfrom(2048)
                    if monitor:
                        self.message_count += 1
                        now = datetime.now().strftime('%H:%M:%S')
                        print(f"[{now}] #{self.message_count} từ {addr[0]} ({len(data)} B)")
                    else:
                        self._process_message(data, addr)
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\n🛑 Dừng nhận")
        finally:
            self.running = False
            self._stats()

    # ---------- Tiện ích ----------
    def _stats(self):
        if self.start_time:
            dur = time.time() - self.start_time
            rate = self.message_count/dur if dur else 0
            print(f"\n📊 THỐNG KÊ • Tổng: {self.message_count} • Thời gian: {dur:.1f}s • {rate:.2f} msg/s")

    def close(self):
        self.leave_multicast_group()
        if self.sock:
            self.sock.close()
            print("🔒 Đã đóng socket")

# ----------------- main -----------------
def main():
    print("="*60)
    print("📡 IPv6 MULTICAST RECEIVER")
    print("="*60)

    # ====== Thông số mặc định (sửa nếu cần) ======
    GROUP = 'ff13::1'
    PORT  = 5007
    IFACE = ''          # '' = interface mặc định, hoặc 'eth0', 'enp3s0', ...

    rx = MulticastReceiverIPv6(GROUP, PORT, IFACE)

    try:
        rx.setup_socket()
        print("1. Nhận chi tiết\n2. Monitor (ngắn gọn)")
        opt = input("Chọn chế độ (1‑2): ").strip()
        if opt == '2':
            rx.receive(monitor=True)
        else:
            rx.receive()
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        rx.close()

if __name__ == "__main__":
    main()
