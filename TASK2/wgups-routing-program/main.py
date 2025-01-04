import delivery_process
from datetime import datetime

def main():
    print("***********************************************")
    print("* WELCOME TO THE WGUPS ROUTING PROGRAM CLI    *")
    print("***********************************************")

    while True:
        print("\n*********************** COMMANDS ***********************")
        print(" - To add a package into the table, type 'a'")
        print(" - For package inquiry, type 'i'")
        print(" - To see package details at a specific time, type 't'")
        print(" - To print details of all packages, type 'd'")
        print(" - To exit or quit the program, type 'q'\n")
        print("*********************** END COMMANDS ***********************")

        command = input("Enter command here (to see all commands type 'h'): ").strip().lower()

        if command == 'q':
            print("Exiting the program. Goodbye!")
            break
        elif command == 'a':
            add_package()
        elif command == 'i':
            package_inquiry()
        elif command == 't':
            package_details_at_time()
        elif command == 'd':
            print_all_packages()
        elif command == 'h':
            continue
        else:
            print("Invalid command. Please try again.")

def add_package():
    print("\nAdding a package to the table...")
    # Logic to add a package would go here.
    pass

def package_inquiry():
    package_id = input("Enter the package ID for inquiry: ").strip()
    package = next((pkg for pkg in delivery_process.all_packages if pkg.id == int(package_id)), None)
    if package:
        print(f"Package {package.id}: {package.status} at {package.delivery_time if package.delivery_time else 'N/A'}")
    else:
        print("Package not found.")

def package_details_at_time():
    try:
        time_str = input("Enter the time to check details (HH:MM AM/PM): ").strip()
        check_time = datetime.strptime(time_str, "%I:%M %p")
        print(f"\nPackage statuses at {check_time.strftime('%I:%M %p')}:")
        for package in delivery_process.all_packages:
            if package.delivery_time and package.delivery_time <= check_time:
                print(f"Package {package.id} delivered at {package.delivery_time.strftime('%I:%M %p')} to {package.address}")
            else:
                print(f"Package {package.id} is {package.status}")
    except ValueError:
        print("Invalid time format. Please enter in HH:MM AM/PM format.")

def print_all_packages():
    print("\nAll package details:")
    for package in delivery_process.all_packages:
        print(f"Package {package.id}: {package.status} at {package.delivery_time if package.delivery_time else 'N/A'}")

if __name__ == "__main__":
    # Ensure that packages are loaded before starting the CLI
    delivery_process.load_packages()
    main()
