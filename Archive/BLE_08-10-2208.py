

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
    def __init__(self,hndl):
        DefaultDelegate.__init__(self)
        self.hndl = hndl

    def handleNotification(self, cHandle, data):
        if self.hndl == cHandle:
            print("Handle : {}, data : {}".format(cHandle, data))


# Bluetooth classes
class BleDevice:

    def __init__(self):
        self.scanner = Scanner().withDelegate(ScanDelegate())

    def Scan(self, time):
        tries = 3
        for i in range(tries):
            try:
                self.devices = self.scanner.scan(time)
            except KeyError as e:
                if i < tries - 1: # i is zero indexed
                    continue
                else:
                    raise
            break

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
                except BTLEException as e:
                    print('Connect to device failed with {} ', format(e))

#    def GetServices(self,):
#
#            services = self.peripheral.getServices()
#            print('Services')
#
#            for service in services:
#                print('My Service : {}'.format(service))
#                characteristics = service.getCharacteristics()
#
#                for characteristic in characteristics:
#                    print('{}'.format(characteristic))
#
#            self.services = services

# Characteristic UUID for Watchdog Only

    def GetCharacteristicsByUUID_WD(self):

        CHARACT_ack = False
        CharacteristicUUID = "7895cecb-a923-4ce4-bc58-27e8ce6e00ea"

        Service_characteristics = self.service.getCharacteristics()

        for characteristic in Service_characteristics:
#            print('My WatchDog Characteristic : {}'.format(characteristic))

            if str(characteristic.uuid) == CharacteristicUUID:
                CHARACT_ack = True
                self.BoogiCharact = characteristic
                print('Characteristic WatchDog Verified')
            else:
                print('Characteristic WatchDog error')

# Service UUID for Watchdog Only
    def GetServiceByUUID_WD(self):
        UUID_ack = False
        ServiceUUID = "1a49d922-e3a9-4b00-9253-c4c72a1bcb5d"

        self.service = self.peripheral.getServiceByUUID(ServiceUUID)
#        print('service found is {}, service searched is {}'.format(str(self.service.uuid), ServiceUUID))

        if str(self.service.uuid) == ServiceUUID:
            UUID_ack = True
#            print('My WatchDog service : {}'.format(self.service.uuid))
            print('Service WatchDog Verified')
            ble.GetCharacteristicsByUUID_WD() 

        else:
            UUID_ack=False
            print('Search WatchDig Service by UUID error')


    def ReadCharacteristic_WD(self):
       Info = self.BoogiCharact.read()
       print('My WD Characteristic value is : {}'.format(Info))


#This function send a RDY to receive data.
    def ReadyToReceiveData(self):

        RdyChar = None
        RdyServiceUUID = '67888895-69db-4168-8df4-9e12a10fa5b7'
        DataCharUUID = '04461336-088e-418e-b8aa-606bdcb8f300'
        RdyCharUUID = '713a155c-5ae2-4604-9ec4-078ad627926e'
        RdyService = self.peripheral.getServiceByUUID(RdyServiceUUID)
        RdyCharacteristics = RdyService.getCharacteristics()

        for Characteristic in RdyCharacteristics:
#            print('All Char are : {}'.format(str(Characteristic.uuid)))

            if Characteristic.uuid == RdyCharUUID:
                RdyChar = Characteristic
                print('Characteristic Data RDY is : {}'.format(RdyChar))
                code = '1'
                bytes1 = bytes(code, 'utf-8')
                RdyHandle = RdyChar.getHandle()
#                print(ghandle)
                RdyChar.write(bytes1)
#                Read = RdyChar.read()
           
            elif Characteristic.uuid == DataCharUUID:
                DataChar = Characteristic
                self.DataHandle = DataChar.getHandle()


#Write to handle 15 ou +1
    def WriteDataToCharacteristic(self):
        self.DataHDL = self.DataHandle + 1
        code = "\x02\x00"
        bytes1 = bytes(code, 'utf-8')
#        print('Writing : {} to HDL : {}'.format(bytes1, self.DataHandle))
        self.peripheral.writeCharacteristic(self.DataHDL,bytes1)


    def ReceivingData(self):
        self.peripheral.setDelegate(NotifyDelegate(self.DataHandle))
        ble.WriteDataToCharacteristic()
        while True:
            if self.peripheral.waitForNotifications(1.0):
                continue


    def ConnectToBoogie(self):
	# Function find & connect to boogie. Then verify if connected to right Service and Characteristic. Finaly reads the characteristic. 
        boogie = ble.FindBoogie()
        ble.ConnectToDevice(boogie)
        ble.GetServiceByUUID_WD()
        ble.ReadCharacteristic_WD()
        ble.ReadyToReceiveData()
        ble.ReceivingData()


#DOIS FAIRE QUE LE BOOGIE VA PAS PLUS LOIN SI NE TROUVE PAS DE DEVICE DU NOM DE BOOG (INCLURE CONNECTTODEVICE DANS FIND BOOGIE etc)


# Main Code ----------------------------------------

ble = BleDevice()
ble.Scan(5.0)

#ble.ListDevices(True)
ble.ConnectToBoogie()
ble.WriteDataToCharacteristic()


# In[19]:

# Using gattlib or pybluez

#service = DiscoveryService()
#devices = service.discover(5)

#for address, name in devices.items():
#    print("name: {}, address: {}".format(name, address)



# Service for confirmation                                                 67888895-69db-4168-8df4-9e12a10fa5b7   
#define COPY_DATA_SERVICE_UUID(uuid_struct)      COPY_UUID_128(uuid_struct,0x67,0x88,0x88,0x95, 0x69,0xdb, 0x41,0x68, 0x8d,0xf4, 0x9e,0x12,0xa1,0x0f,0xa5,0xb7)
# Send to this char RDY                                                    713a155c-5ae2-4604-9ec4-078ad627926e
#define COPY_READY_CHAR_UUID(uuid_struct)        COPY_UUID_128(uuid_struct,0x71,0x3a,0x15,0x5c, 0x5a,0xe2, 0x46,0x04, 0x9e,0xc4, 0x07,0x8a,0xd6,0x27,0x92,0x6e)
# Reception de donné                                                       04461336-088e-418e-b8aa-606bdcb8f300
#define COPY_DATA_CHAR_UUID(uuid_struct)         COPY_UUID_128(uuid_struct,0x04,0x46,0x13,0x36, 0x08,0x8e, 0x41,0x8e, 0xb8,0xaa, 0x60,0x6b,0xdc,0xb8,0xf3,0x00)

# WatchDog Service for Confirmation 
#define COPY_WATCH_DOG_SERVICE_UUID(uuid_struct) COPY_UUID_128(uuid_struct,0x1a,0x49,0xd9,0x22, 0xe3,0xa9, 0x4b,0x00, 0x92,0x53, 0xc4,0xc7,0x2a,0x1b,0xcb,0x5d)
# WatchDog Characteristic
#define COPY_WATCH_DOG_CHAR_UUID(uuid_struct)    COPY_UUID_128(uuid_struct,0x78,0x95,0xce,0xcb, 0xa9,0x23, 0x4c,0xe4, 0xbc,0x58, 0x27,0xe8,0xce,0x6e,0x00,0xea)
