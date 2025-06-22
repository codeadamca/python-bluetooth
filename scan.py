'''
import asyncio
from bleak import BleakScanner


async def scan_bluetooth_devices():
    
    print("Scanning for Bluetooth devices...")
    
    devices = await BleakScanner.discover()
    
    if devices:
        print(f"Found {len(devices)} devices:")
        for device in devices:
            print(f"  Address: {device.address}, Name: {device.name if device.name else 'Unknown'}")
    else:
        print("No Bluetooth devices found.")

if __name__ == "__main__":
        asyncio.run(scan_bluetooth_devices())
'''

import asyncio
from bleak import BleakScanner

import socket
print(socket.gethostname())

def extract_message(original_data):

    for mid, data in original_data:
        print(f"Raw data: {data.hex()}")

        # Strip all non-ASCII prefix bytes
        ascii_bytes = bytes(b for b in data if 32 <= b <= 126)

        try:
            ascii_text = ascii_bytes.decode('ascii')
            print(f"ASCII text: {ascii_text}")
        except UnicodeDecodeError:
            print("Could not decode ASCII text.")

def detection_callback(device, advertisement_data):

    # if device.name == "sp_alpha":

    # if advertisement_data.manufacturer_data and 819 in advertisement_data.manufacturer_data:

    if True:

        print(f"\nDevice: {device.name} ({device.address})")
        print("  RSSI:", advertisement_data.rssi)
        print("  Local Name:", advertisement_data.local_name)
        print("  Manufacturer Data:", advertisement_data.manufacturer_data)
        print("  Service Data:", advertisement_data.service_data)
        print("  Service UUIDs:", advertisement_data.service_uuids)
        print("  TX Power:", advertisement_data.tx_power)

        extract_message(advertisement_data.manufacturer_data.items())


async def main():
    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    await asyncio.sleep(10)  # scan for 10 seconds
    await scanner.stop()

asyncio.run(main())
