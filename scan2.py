import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)
        print(device.name)

if __name__ == "__main__":
    asyncio.run(main())