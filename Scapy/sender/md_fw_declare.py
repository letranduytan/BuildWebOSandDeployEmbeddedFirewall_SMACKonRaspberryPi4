from scapy.all import *
from scapy.layers.inet import *
from scapy.layers.inet6 import *
from random import randint
from netaddr import *
import binascii
import sys
import signal
from threading import Thread

# -------------------- Interface --------------------
IFACE = "Ethernet"

# -------------------- Thread / Packet Settings --------------------
PKT_COUNT = 5
FROM_PORT = 1
TO_PORT = 65536

# -------------------- MAC Addresses --------------------
SRC_MAC = "B4:45:06:42:83:99"
DST_MAC = "d8:3a:dd:a4:bf:02"# Board
INVALID_SRC_MAC = "fa:fb:fc:fd:fe:ff"  # Invalid MAC for fuzzing

# -------------------- VLAN ID --------------------
VLAN_ID = 5

# -------------------- IPv6 Addresses --------------------
VALID_SRC_IPv6 = "fd53:1234:5678:5::10"
VALID_DST_IPv6 = "fd53:1234:5678:5::14"
INVALID_SRC_IPv6 = "fd53:1234:5678:3::12"  # Invalid IPv6
INVALID_DST_IPv6 = "fd53:1234:5678:3::15"  # Invalid IPv6

VALID_DST_MULTICAST = "ff02::1"
INVALID_DST_MULTICAST = "ff02::2"

# -------------------- Ports --------------------
VALID_SPORT = 13344
VALID_DPORT = 13344
INVALID_SPORT = 13456
INVALID_DPORT = 13456

PORT_RANGE = (1000, 65535)

# -------------------- Protocol Type --------------------
pro_type = TCP

# -------------------- Layers --------------------
dot1q = Dot1Q(vlan=VLAN_ID)

# -------------------- Payload --------------------
payload_default = """sh:ip link add link eth0 name eth0.5 type vlan id 5 &&
ip link set dev eth0.5 address AA:BB:CC:DD:EE:FF &&
ip link set dev eth0.5 up"""


# -------------------- Packets --------------------
PKT_Default_Receive = Ether(dst=DST_MAC)/dot1q/IPv6(src=VALID_SRC_IPv6, dst=VALID_DST_IPv6)/pro_type(sport=VALID_SPORT, dport=VALID_DPORT)/Raw(load=payload_default)

PKT_Default_Send = Ether(dst=SRC_MAC, src=DST_MAC)/dot1q/IPv6(src=VALID_DST_IPv6, dst=VALID_SRC_IPv6)/pro_type(sport=VALID_DPORT, dport=VALID_SPORT)/Raw(load=payload_default)
