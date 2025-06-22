import time
import objc

from Foundation import NSObject, NSData, NSLog, NSRunLoop, NSDate
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
        if peripheral.state() == 5:
            print("Bluetooth is powered ON.")
            self.ready = True
        else:
            print(f"Bluetooth state: {peripheral.state()}")

# Set up delegate and peripheral
delegate = PeripheralDelegate.alloc().init()
peripheral = CBPeripheralManager.alloc().initWithDelegate_queue_options_(delegate, None, None)

# Wait for CoreBluetooth to call back with state change
print("Waiting for Bluetooth to power on...")
while not delegate.ready:
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))

# Prepare manufacturer data payload
manufacturer_id = (919).to_bytes(2, 'little')
# manufacturer_id = (39).to_bytes(2, 'little')

payload = bytes([
    39,  # channel
    0,   # single value
    (5 << 5) | len(b"green"),
    *b"green"
])
adv_data = manufacturer_id + payload

advertisement = {
    CBAdvertisementDataManufacturerDataKey: NSData.dataWithBytes_length_(adv_data, len(adv_data))
}

# Start advertising
print("Starting BLE advertisement...")
peripheral.startAdvertising_(advertisement)

# Run loop for 60 seconds
start_time = time.time()
while time.time() - start_time < 60:
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))

print("Stopping advertisement.")
peripheral.stopAdvertising()
