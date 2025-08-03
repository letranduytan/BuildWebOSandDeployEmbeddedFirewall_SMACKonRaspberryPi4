from md_fw_declare import *
from md_fw_menu import *

# PKT_Default_Receive[IPv6].src=INVALID_SRC_IPv6 # This line seems to be a comment/example, not active code

def print_infor():
    try:
        global PKT_Default_Receive2
        print("\n----------Packet-information-------------")
        PKT_Default_Receive.show()
    except Exception as ex:
        print("Error:" + str(ex))

# 16.1.13.4 Undefined target IPv6 address
def send_packet():
    global PKT_Default_Receive
    try:
        PKT_Default_Receive.show()
        sendp(PKT_Default_Receive, iface=IFACE)
    except Exception as ex:
        print("Error: Please Connect Ethernet..." + str(ex))

def main():
    cloop = True
    while cloop:
        try:
            choice = print_menu()
            if int(choice) == 1:
                print_infor()
            elif int(choice) == 2:
                send_packet()
            elif int(choice) == 0:
                cloop = False
        except KeyboardInterrupt:
            print('\nThanks! See you later!\n\n')
            cloop = False

if __name__ == '__main__':
    main()