import objc
import time
from Foundation import NSObject, NSData, NSRunLoop, NSDate
from CoreBluetooth import (
    CBPeripheralManager,
    CBAdvertisementDataManufacturerDataKey,
    CBAdvertisementDataLocalNameKey,
)

class Delegate(NSObject):
    def init(self):
        self = objc.super(Delegate, self).init()
        self.ready = False
        return self

    def peripheralManagerDidUpdateState_(self, peripheral):
        if peripheral.state() == 5:
            print("Bluetooth powered ON")
            self.ready = True
        else:
            print(f"Bluetooth state: {peripheral.state()}")

# Setup delegate and peripheral manager
delegate = Delegate.alloc().init()
peripheral = CBPeripheralManager.alloc().initWithDelegate_queue_options_(delegate, None, None)

print("Waiting for Bluetooth...")
while not delegate.ready:
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))

# Test payload: manufacturer ID 0x0027 (39), 1-byte payload 0x7B (123)
manufacturer_id = (919).to_bytes(2, 'little')

# payload = b'\x7B'  # 123

payload = bytes([
    39,  # channel
    0,   # single value
    (5 << 5) | len(b"green"),
    *b"green"
])

raw = manufacturer_id + payload

# Convert to NSData for CoreBluetooth
adv_nsdata = NSData.dataWithBytes_length_(raw, len(raw))

advertisement = {
    CBAdvertisementDataManufacturerDataKey: adv_nsdata,
    CBAdvertisementDataLocalNameKey: "green-test"
}

print("Starting advertisement...")
peripheral.startAdvertising_(advertisement)

start = time.time()
while time.time() - start < 60:
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))

print("Stopping advertisement.")
peripheral.stopAdvertising()
