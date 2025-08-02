mport socket

MULTICAST_GROUP = 'ff02::2222'
PORT = 10002

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

message = "Hello from Sender 2 to Group 2!"

sock.sendto(message.encode(), (MULTICAST_GROUP, PORT))

print(f'Sent: "{message}" to {MULTICAST_GROUP}:{PORT}')

~