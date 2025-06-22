import objc
import time
from Foundation import NSObject, NSLog, NSData
from CoreBluetooth import CBCentralManager, CBPeripheralManager, CBAdvertisementDataManufacturerDataKey, CBAdvertisementDataLocalNameKey

class PeripheralDelegate(NSObject):

    def peripheralManagerDidUpdateState_(self, peripheral):

        # if peripheral.state() == 5:  # 5 = Powered On

        print("Peripheral is powered on, starting advertisement...")

        # Manufacturer-specific data (channel 39 = 0x0027)
        data = bytes([
            39,  # channel
            0,  # indicates only one value/not a tuple
            (5 << 5) | len(b"green"),  # type/length header: 5=str
            *b"green",  # str data
        ])
        manufacturer_id = (919).to_bytes(2, 'little')  # 0x27 = 39
        adv_data = manufacturer_id + data

        adv_dict = {
            CBAdvertisementDataManufacturerDataKey: NSData.dataWithBytes_length_(adv_data, len(adv_data)),
            # CBAdvertisementDataLocalNameKey: "MacColor"
        }

        peripheral.startAdvertising_(adv_dict)

peripheral_delegate = PeripheralDelegate.alloc().init()

peripheral = CBPeripheralManager.alloc().initWithDelegate_queue_options_(peripheral_delegate, None, None)

# Keep it running for 60 seconds
for _ in range(60):
    time.sleep(1)
    
