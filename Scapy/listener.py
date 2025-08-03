from scapy.all import *
import subprocess

# Giao diện mạng của Raspberry (thay nếu cần)
INTERFACE = "eth0"

# Địa chỉ MAC hợp lệ của máy gửi (nếu muốn filter)
TRUSTED_MACS = ["xx:xx:xx:xx:xx:xx", "d8:3a:dd:a4:bf:02"]  # hoặc bỏ lọc

# Xử lý gói tin nhận được
def process_packet(pkt):
    if pkt.haslayer(IPv6) and pkt.haslayer(Raw):
        src_mac = pkt[Ether].src
        if src_mac not in TRUSTED_MACS:
            print(f"[!] Gói tin bị bỏ qua từ MAC không tin cậy: {src_mac}")
            return

        payload = pkt[Raw].load.decode(errors='ignore').strip()
        print(f"[+] Nhận payload từ {src_mac}: {payload}")

        # Phân tích payload theo định dạng key=value
        try:
            key, value = payload.split("=")
            if key == "IPV6":
                change_ipv6(value)
            elif key == "MAC":
                change_mac(value)
            elif key == "VLAN":
                change_vlan(value)
            else:
                print("[!] Lệnh không hợp lệ.")
        except Exception as e:
            print(f"[!] Payload không hợp lệ: {e}")

# Thay đổi địa chỉ IPv6
def change_ipv6(ipv6_addr):
    print(f"[*] Đang thay IPv6 thành: {ipv6_addr}")
    subprocess.run(f"sudo ip -6 addr flush dev {INTERFACE}", shell=True)
    subprocess.run(f"sudo ip -6 addr add {ipv6_addr}/64 dev {INTERFACE}", shell=True)

# Thay đổi địa chỉ MAC
def change_mac(mac_addr):
    print(f"[*] Đang thay MAC thành: {mac_addr}")
    subprocess.run(f"sudo ip link set dev {INTERFACE} down", shell=True)
    subprocess.run(f"sudo ip link set dev {INTERFACE} address {mac_addr}", shell=True)
    subprocess.run(f"sudo ip link set dev {INTERFACE} up", shell=True)

# Gán VLAN ID (giả sử bạn đã cấu hình VLAN trước)
def change_vlan(vlan_id):
    print(f"[*] VLAN ID thay đổi thành: {vlan_id}")
    subprocess.run(f"sudo vconfig add {INTERFACE} {vlan_id}", shell=True)
    subprocess.run(f"sudo ip link set up {INTERFACE}.{vlan_id}", shell=True)

# Bắt gói
print(f"[+] Đang lắng nghe gói tin trên {INTERFACE}...")
sniff(iface=INTERFACE, prn=process_packet, store=0)