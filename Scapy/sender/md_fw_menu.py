def print_menu():
    cloop = True
    while cloop:
        print(22 * "-", "MENU", 22 * "-")
        print("\t1. [Infor] {:<24}".format("Packet information"))
        print("\t2. [Send]  {:<24}".format("Packet Send"))
        print("\t0. [Exit]  {:<24}".format("Exit"))
        print(50 * "-")
        
        try:
            choice = input("Enter your choice [0-2]: ")
            if choice.isdigit() and 0 <= int(choice) <= 2:
                cloop = False
            else:
                print("Invalid choice. Please enter 0, 1, or 2.\n")
        except ValueError:
            print("Invalid input. Please enter a number.\n")
            
    return choice


if __name__ == '__main__':
    choice = print_menu()
    print(f"You selected option: {choice}")
