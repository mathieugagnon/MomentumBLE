

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



# Using bluepy

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass


class NotifyDelegate(DefaultDelegate):
    def __init__(self,hndl):
        DefaultDelegate.__init__(self)
        self.hndl = hndl

    def handleNotification(self, cHandle, data):
        if self.hndl == cHandle:
            print("Handle : {}, data : {}".format(cHandle, data))
        else:
            print("self.hndl != cHandle")
 

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

#        self.boogie = dev
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


# Service UUID for Watchdog Only
    def GetServiceByUUID_WD(self, S_UUID):
        UUID_ack = False      
        try:      
            self.service = self.peripheral.getServiceByUUID(S_UUID)
        except error as e:
            print('Error in finding service UUID for WD with {}',format(e))

        if str(self.service.uuid) == S_UUID:
            UUID_ack = True
            print('Service WatchDog Verified')
        else:
            UUID_ack=False
            print('Search WatchDig Service by UUID error')


# Characteristic UUID for Watchdog Only
    def GetCharacteristicsByUUID_WD(self,C_UUID):
        CHARACT_ack = False
        BoogieWD_Characteristic = None
        try:
            Service_characteristics = self.service.getCharacteristics()
        except error as e:
            print('Error in finding Characteristic UUID for WD with : {}',format(e))
        
        for characteristic in Service_characteristics:
            if str(characteristic.uuid) == C_UUID:
                CHARACT_ack = True
                BoogieWD_Characteristic = characteristic
                print('Characteristic WatchDog Verified')
            else:
                print('Characteristic WatchDog error')
        
        return BoogieWD_Characteristic       


# Read Characteristics for Watchdog Only
    def ReadCharacteristic_WD(self, Boogie_Characteristic_WD):
        try:
            Info = Boogie_Characteristic_WD.read()
            print('My WD Characteristic value is : {}'.format(Info))
        except error as e:
            print('Error in reading Watchdog Characteristic with : {}'.format(e))


#This function send a RDY to receive data. (VERIFY THIS FONCTION LAST)
    def ReadyToReceiveData(self, RdyServiceUUID, RdyCharUUID):
        RdyCharacteristic = None
                
        RdyService = self.peripheral.getServiceByUUID(RdyServiceUUID)
        RdyCharacteristics = RdyService.getCharacteristics()       
        for Characteristic in RdyCharacteristics:
            if Characteristic.uuid == RdyCharUUID:
                RdyCharacteristic = Characteristic
                print('Characteristic Data RDY is : {}'.format(RdyCharcteristic))
    # Write random data to characteristic to verify if communication is valid. 
                code = '1'
                bytes1 = bytes(code, 'utf-8')
                RdyHandle = RdyCharacteristic.getHandle()
                RdyCharacteristic.write(bytes1)


# Get handle from service and data characteristic
    def SubcribeToIndication(self, ServiceUUID, DataCharacteristicUUID):
        self.DataHandle = None

        Service = self.peripheral.getServiceByUUID(ServiceUUID)
        Characteristics = Service.getCharacteristics()
        for Characteristic in Characteristics:
            if Characteristic.uuid == DataCharacteristicUUID:
                self.DataHandle = Characteristic.getHandle()
                self.DataHandle = self.DataHandle + 1
                print('Data Handle # is : {}'.format(self.DataHandle))


    def InitializeDataTransfert(self):
        code = "\x02\x00"
        bytes1 = bytes(code, 'utf-8')
        try:
            self.peripheral.writeCharacteristic(self.DataHandle,bytes1)
        except error as e:
            print('Error in Data transfert initialization : {}'.format(e))


    def ReceivingData(self):
        self.peripheral.setDelegate(NotifyDelegate(self.DataHandle))
        while True:
            if  self.peripheral.waitForNotifications(10)== False:
                break


# Main Code -----------------------------------------------------------

ble = BleDevice()

ble.Scan(5.0)

boogie = ble.FindBoogie()

#Find device named boogie in device list
ble.ConnectToDevice(boogie)

#Find Watchdog service from Device and validate the UUID
S_UUID = "1a49d922-e3a9-4b00-9253-c4c72a1bcb5d"
ble.GetServiceByUUID_WD(S_UUID)

#Find Watchdog characteristic and validate the UUID
C_UUID =  "7895cecb-a923-4ce4-bc58-27e8ce6e00ea"
BoogieCharacteristic= ble.GetCharacteristicsByUUID_WD(C_UUID) 

#Read WD Characteristic value and confirm the value
ble.ReadCharacteristic_WD(BoogieCharacteristic) 

#
ServiceUUID = '67888895-69db-4168-8df4-9e12a10fa5b7'
RdyCharUUID = '713a155c-5ae2-4604-9ec4-078ad627926e'
#ble.ReadyToReceiveData(ServiceUUID, RdyCharUUID)
#

#Find Data Handle from data characteristic UUID. Prepare Handle+1 for writing
DataCharUUID = '04461336-088e-418e-b8aa-606bdcb8f300'
ServiceUUID = '67888895-69db-4168-8df4-9e12a10fa5b7'
ble.SubcribeToIndication(ServiceUUID, DataCharUUID)

#Initialize Data transfert by writing 2 in bytes to the data characteristic
ble.InitializeDataTransfert()

#Enter a while loop to receive data. exit the while loop when timeout(10sec) is reach.
ble.ReceivingData()


#ble.ListDevices(True)


#ble.WriteDataToCharacteristic()



