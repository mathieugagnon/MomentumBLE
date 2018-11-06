

# coding: utf-8

# In[16]:

import platform
#from bluetooth.ble import DiscoveryService from gattlib import DiscoveryService, GATTRequester
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
           # print("Device {} ({}){}, RSSI={} dB".format(dev.addr, dev.addrType, ' [Connectable]' if dev.connectable else '', dev.rssi))
            
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
           # print('EXIT IS : {}'.format(device))
            if device is None:
                print("No device detected")
            else:
                try:
                    self.peripheral = Peripheral(device)
                    print("Connected to device")
                except BTLEException:
                    print('Connection failed')

    def GetServices(self):

            services = self.peripheral.getServices()
            print('Services')

            for service in services:
                print('My Service : {}'.format(service))
                characteristics = service.getCharacteristics()

                for characteristic in characteristics:
                    print('{}'.format(characteristic))
         
            self.services = services
           

    def ConnectToBoogie(self):
	# Function find & connect to boogie. Validate connection with a known service and characteristic
        # Service : 1a49d922-e3a9-4b00-9253-c4c72a1bcb5d      Characteristic : 7895cecb-a923-4ce4-bc58-27e8ce6e00ea   Expected value : (0x32) or if char = (2)

        UUID_ack = False
        CHARACT_ack = False
        UUIDval = "1a49d922-e3a9-4b00-9253-c4c72a1bcb5d"
        CHARACTval = "Characteristic <7895cecb-a923-4ce4-bc58-27e8ce6e00ea>"

        boogie = ble.FindBoogie()
        ble.ConnectToDevice(boogie)

        print('Trying to verify')
        try:
            serviceUUID = self.peripheral.getServiceByUUID(UUIDval)
            print('My UUID service : {}'.format(serviceUUID))
            UUID_ack = True
        except BTLEException:
            print('Service not found')
            UUID_ack = False

        if UUID_ack is True:
            Service_charact = serviceUUID.getCharacteristics()
           # print('Caracteristic list : {}'.format(Service_charact))
            
            for characteristic in Service_charact:
                print('My CHARACT : {}'.format(characteristic))
                print(characteristic)

            if characteristic == CHARACTval:
                CHARACT_ack = True
        print('UUIDack is : {}, CHARACTack is : {}'.format(UUID_ack, CHARACT_ack))

# Main Code

ble = BleDevice()
ble.Scan(5.0)
#ble.ListDevices(True)
ble.ConnectToBoogie()


# In[19]:

# Using gattlib or pybluez

#service = DiscoveryService()
#devices = service.discover(5)

#for address, name in devices.items():
#    print("name: {}, address: {}".format(name, address)
