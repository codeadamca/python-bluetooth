import os
import time

def advertise(name="BrickPiBLE"):
    # Stop previous advertising
    os.system("sudo hciconfig hci0 noleadv")
    
    # Set the device name (optional)
    os.system(f"sudo hciconfig hci0 name {name}")
    
    # Set custom advertising data:
    # Format: Length, Type, Data (Here "BrickPi-BLE" as device name)
    os.system("sudo hcitool -i hci0 cmd 0x08 0x0008 1e 02 01 06 0b 09 42 72 69 63 6b 50 69 2d 42 4c 45")
    
    # Enable advertising (LE General Discoverable)
    os.system("sudo hciconfig hci0 leadv 3")
    
    print(f"Advertising as {name}")

advertise()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping advertising...")
    os.system("sudo hciconfig hci0 noleadv")
