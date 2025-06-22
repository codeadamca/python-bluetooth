import objc
import time
from Foundation import NSObject, NSData, NSRunLoop, NSDate
from CoreBluetooth import (
    CBPeripheralManager,
    CBAdvertisementDataManufacturerDataKey,
)

class PeripheralDelegate(NSObject):
    def init(self):
        self = objc.super(PeripheralDelegate, self).init()
        if self is None:
            return None
        self.ready = False
        return self

    def peripheralManagerDidUpdateState_(self, peripheral):
        if peripheral.state() == 5:  # Powered On
            print("Bluetooth is powered ON")
            self.ready = True
        else:
            print(f"Bluetooth state: {peripheral.state()}")

# Set up delegate and peripheral manager
delegate = PeripheralDelegate.alloc().init()
peripheral = CBPeripheralManager.alloc().initWithDelegate_queue_options_(delegate, None, None)

# Wait until Bluetooth is ready
print("Waiting for Bluetooth...")
while not delegate.ready:
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))

# --- SET THIS TO MATCH YOUR SPIKE ---
manufacturer_id = (39).to_bytes(2, 'little')  # Use 39 (0x0027) for testing
payload = bytes([123])  # Just send 1 byte for now

adv_data = manufacturer_id + payload

advertisement = {
    CBAdvertisementDataManufacturerDataKey: NSData.dataWithBytes_length_(adv_data, len(adv_data))
}

# Start advertising
print("Advertising manufacturer data with ID 39...")
peripheral.startAdvertising_(advertisement)

# Run for 60 seconds
start_time = time.time()
while time.time() - start_time < 60:
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))

peripheral.stopAdvertising_()
print("Stopped advertising.")
