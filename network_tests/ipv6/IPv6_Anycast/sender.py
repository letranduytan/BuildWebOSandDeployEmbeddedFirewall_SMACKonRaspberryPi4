import subprocess

def get_ipv6_anycast():
    result = subprocess.run(['ip', '-6', 'addr', 'show'], stdout=subprocess.PIPE)
    output = result.stdout.decode()

    anycast_addresses = []

    lines = output.split('\n')
    for line in lines:
        line = line.strip()
        if 'scope global anycast' in line:
            parts = line.split()
            addr = parts[1]
            anycast_addresses.append(addr)

    return anycast_addresses

if __name__ == '__main__':
    anycast_list = get_ipv6_anycast()
    if anycast_list:
        print("Anycast IPv6 addresses found:")
        for addr in anycast_list:
            print(addr)
    else:
        print("No Anycast IPv6 addresses found.")

~