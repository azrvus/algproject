from datetime import datetime, timedelta

class Package:
    def __init__(self, package_id, address, delivery_deadline, city, zip_code, weight, special_note):
        self.id = package_id
        self.address = address
        self.delivery_deadline = delivery_deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.special_note = special_note
        self.status = "At Hub"
        self.delivery_time = None
        self.truck_id = None

class Truck:
    def __init__(self, truck_id, speed, max_packages):
        self.id = truck_id
        self.speed = speed  # miles per hour
        self.max_packages = max_packages
        self.packages = []
        self.route = []
        self.mileage = 0
        self.current_time = datetime.strptime("08:00 AM", "%I:%M %p")

    def load_package(self, package):
        if len(self.packages) < self.max_packages:
            self.packages.append(package)
            package.truck_id = self.id

    def deliver_packages(self):
        for destination in self.route:
            distance = destination['distance']  # Distance to the next stop
            time_to_travel = timedelta(hours=distance / self.speed)
            self.current_time += time_to_travel
            self.mileage += distance

            for package in destination['packages']:
                package.status = "Delivered"
                package.delivery_time = self.current_time

# Initialize all packages
all_packages = []

# Load all packages

def load_packages():
    global all_packages
    all_packages.append(Package(1, "123 Elm St", "10:30 AM", "Salt Lake City", "84101", 5, ""))
    all_packages.append(Package(2, "456 Oak St", "EOD", "Salt Lake City", "84102", 7, ""))
    all_packages.append(Package(9, "Wrong Address", "EOD", "Salt Lake City", "84103", 2, "Address corrected at 10:20 AM"))

# Update Package 9 Address

def update_package_9_address(current_time):
    for package in all_packages:
        if package.id == 9 and current_time >= datetime.strptime("10:20 AM", "%I:%M %p"):
            package.address = "410 S. State St., Salt Lake City, UT 84111"
            print(f"Package 9 address updated at {current_time.strftime('%I:%M %p')}")

# Simulate delivery process

def simulate_delivery():
    truck_1 = Truck(truck_id=1, speed=18, max_packages=16)

    # Load all packages onto the truck
    for package in all_packages:
        truck_1.load_package(package)

    # Define route for Truck 1
    truck_1.route = [
        {"distance": 5, "packages": truck_1.packages},
    ]

    while truck_1.route:
        destination = truck_1.route.pop(0)
        distance = destination['distance']
        time_to_travel = timedelta(hours=distance / truck_1.speed)
        truck_1.current_time += time_to_travel
        truck_1.mileage += distance

        print(f"Current time: {truck_1.current_time.strftime('%I:%M %p')}")
        
        # Update Package 9's address dynamically
        update_package_9_address(truck_1.current_time)

        for package in destination['packages']:
            # Skip Package 9 if the address has not been updated yet
            if package.id == 9 and package.address == "Wrong Address":
                print(f"Skipping Package {package.id} as address has not been updated yet.")
                continue

            # Deliver the package
            package.status = "Delivered"
            package.delivery_time = truck_1.current_time
            print(f"Delivered Package {package.id} to {package.address} at {package.delivery_time.strftime('%I:%M %p')}")

        # Retry delivery for Package 9 if address has been updated
        for package in truck_1.packages:
            if package.status == "At Hub" and package.id == 9 and package.address != "Wrong Address":
                print(f"Retrying delivery for Package {package.id} after address update.")
                package.status = "Delivered"
                package.delivery_time = truck_1.current_time
                print(f"Delivered Package {package.id} to {package.address} at {package.delivery_time.strftime('%I:%M %p')}")

    print(f"Total mileage for Truck {truck_1.id}: {truck_1.mileage} miles")





if __name__ == "__main__":
    load_packages()
    simulate_delivery()
