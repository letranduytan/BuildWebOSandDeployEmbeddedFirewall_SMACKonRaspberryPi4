import socket
import logging
import datetime

# Set up basic logger
def setup_logger(name="nettest", log_file="network_test.log", level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(console)

    return logger


# Create a UDP socket
def create_udp_socket(ip_version=4):
    if ip_version == 4:
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    elif ip_version == 6:
        return socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    else:
        raise ValueError("Invalid IP version. Use 4 or 6.")


# Create a multicast receiver socket (IPv4 or IPv6)
def create_multicast_receiver(multicast_group, port, ip_version=4, interface_ip='0.0.0.0'):
    if ip_version == 4:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((interface_ip, port))
        mreq = socket.inet_aton(multicast_group) + socket.inet_aton(interface_ip)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    elif ip_version == 6:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', port))
        # Use interface index 0 (default)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP,
                        socket.inet_pton(socket.AF_INET6, multicast_group) + b'\x00' * 4)
    else:
        raise ValueError("Invalid IP version")
    
    return sock


# Timestamped message
def timestamped_message(msg: str) -> str:
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"[{now}] {msg}"
