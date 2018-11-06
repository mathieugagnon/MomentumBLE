
# coding: utf-8

# In[16]:

import platform
#from bluetooth.ble import DiscoveryService
#from gattlib import DiscoveryService, GATTRequester
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEException
import bluepy

print("---------------")
print("Python : " + platform.python_version())
#print("Bluepy : " + bluepy.__version__)
print("---------------")


# Using bluepy

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass
        #if isNewDev:
        #    print("Discovered device", dev.addr)
        #elif isNewData:
        #    print("Received new data from", dev.addr)

class NotifyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    
    def handleNotification(self, cHandle, data):
        print("Handle : {}, data : {}".format(cHandle, data))

# Bluetooth classes

class BleDevice:
    def __init__(self):
        self.scanner = Scanner().withDelegate(ScanDelegate())
    
    def Scan(self, time):
        self.devices = self.scanner.scan(time)

    def ListDevices(self, scan_data_flag):
        for dev in self.devices:
            print("Device {} ({}){}, RSSI={} dB".format(dev.addr, dev.addrType, ' [Connectable]' if dev.connectable else '', dev.rssi))
            
            if scan_data_flag:
                for (adtype, desc, value) in dev.getScanData():
                    print("  {} {} = {}".format(adtype, desc, value))

    def FindBoogie(self):

        boogie = None

        for dev in self.devices:
            for (adtype, desc, value) in dev.getScanData():
                if adtype == 9:
                    if value == "Boogie":
                        boogie = dev

        self.boogie = dev
        return boogie

    def ConnectToDevice(self, device):
        # Function returns Connected to device when device is not there

        try:
            self.peripheral = Peripheral(device)
            print("Connected to device")
        except BTLEException:
            print('Connection failed')

    def GetServices(self):

            services = self.peripheral.getServices()
            
            print('Services')

            for service in services:
                print('{}'.format(service))

                characteristics = service.getCharacteristics()

                for characteristic in characteristics:
                    print('{}'.format(characteristic))

# Main Code

ble = BleDevice()
ble.Scan(5.0)
#ble.ListDevices(True)
boogie = ble.FindBoogie()
ble.ConnectToDevice(boogie)
ble.GetServices()

# In[19]:

# Using gattlib or pybluez

#service = DiscoveryService()
#devices = service.discover(5)

#for address, name in devices.items():
#    print("name: {}, address: {}".format(name, address))
