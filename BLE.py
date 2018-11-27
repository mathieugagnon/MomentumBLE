

# coding: utf-8

# In[16]:

import platform
#from bluetooth.ble import DiscoveryService from gattlib import DiscoveryService, GATTRequester
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEException
import bluepy

# Service for confirmation                                                  67888895-69db-4168-8df4-9e12a10fa5b7
#define COPY_DATA_SERVICE_UUID(uuid_struct)      COPY_UUID_128(uuid_struct,0x67,0x88,0x88,0x95, 0x69,0xdb, 0x41,0x68, 0x8d,0xf4, 0x9e,0x12,0xa1,0x0f,0xa5,0xb7)


# Send to this UUID     LENGTH DATA IN                                      713a155c-5ae2-4604-9ec4-078ad627926e
#define COPY_DATAIN_CHAR_UUID(uuid_struct)        COPY_UUID_128(uuid_struct,0x71,0x3a,0x15,0x5c, 0x5a,0xe2, 0x46,0x04, 0x9e,0xc4, 0x07,0x8a,0xd6,0x27,0x92,0x6e)

#                                                                           e7a87ad7-9ce0-40d0-896f-7fbc3d10d9ff
#DATA IN (send to proto on this UUID) (VOIR FB)   UUID (0xe7,0xa8,0x7a,0xd7, 0x9c,0xe0, 0x40,0xd0, 0x89,0x6f, 0x7f,0xbc,0x3d,0x10,0xd9,0xff)    


# Reception de donné                                                       04461336-088e-418e-b8aa-606bdcb8f300
#define COPY_DATA_CHAR_UUID(uuid_struct)         COPY_UUID_128(uuid_struct,0x04,0x46,0x13,0x36, 0x08,0x8e, 0x41,0x8e, 0xb8,0xaa, 0x60,0x6b,0xdc,0xb8,0xf3,0x00)

# WatchDog Service for Confirmation
#define COPY_WATCH_DOG_SERVICE_UUID(uuid_struct) COPY_UUID_128(uuid_struct,0x1a,0x49,0xd9,0x22, 0xe3,0xa9, 0x4b,0x00, 0x92,0x53, 0xc4,0xc7,0x2a,0x1b,0xcb,0x5d)
   

max_size = 20
index = 0
MaxLength = 2**(8+8+8+8)
#__BleDataInBuffer__ = bytearray()
__BleDataInBuffer__ = []
__DeviceConnection__ = False




def filldatabuffer(data):
    sizeData = len(data)
    if sizeData > 20:
        print("Data buffer too long")   
    else:
        __BleDataInBuffer__.extend(data)    
        # print("{}".format(databuffer))
        # print(self.Mydata)
# Fill buffer with data and verify length


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

    
    def handleNotification(self, cHandle, dataIN):
        if self.hndl == cHandle:           
#            print("Handle : {}, data : {}".format(cHandle, data))
            filldatabuffer(dataIN)
        
        else:
            print("Wrong handle called.")
            print("self.hndl : {} != cHandle : {}".format(self.hndl, cHandle))



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
        if self.devices is not None:
            for dev in self.devices:
                for (adtype, desc, value) in dev.getScanData():
                    if adtype == 9:
                        if value == "Boogie":
                            boogie = dev
                            print('OK : Blackbox Device Found')
        else:
            print('ERROR : No Device found at all')

        if boogie is None:
            print('ERROR : Device not found in scan list')
        
        return boogie


    def ConnectToDevice(self, device):
        # Function returns True of False if Boogie device is connected or not 
           # print('EXIT IS : {}'.format(device))
            
            
            if device is None:
                print('ERROR : No device detected')
            else:
                try:
                    self.peripheral = Peripheral()
                    self.peripheral.connect(device)
                    print('OK : Connected to device')
                    __DeviceConnection__ = True

                except BTLEException as e:
                    print('ERROR : Connection to device failed with exception : {}'.format(e))



    def DisconnectFromDevice(self,device):
        if device is not None:
            try:
                self.peripheral.disconnect()
                __DeviceConnection__ = False
                print("OK : Device Disconnected")
            except Exception as e:
                print("ERROR : Failed to disconnect Device")
        else:
          print("ERROR : No device to disconnect from")
        


# Service UUID for Watchdog Only
    def GetServiceByUUID_WD(self, S_UUID):
        UUID_ack = False      
        try:      
            self.service = self.peripheral.getServiceByUUID(S_UUID)
            if str(self.service.uuid) == S_UUID:
                UUID_ack = True
                print('OK : Service WatchDog Verified')
            else:
                UUID_ack=False
                print('ERROR : Service WatchDog UUID not found in available service')

        except Exception as e:
            print('ERROR : Finding Watchdog Service UUID failed with exception : {}'.format(e))


# Characteristic UUID for Watchdog Only
    def GetCharacteristicsByUUID_WD(self,C_UUID):
        CHARACT_ack = False
        BoogieWD_Characteristic = None
        try:
            Service_characteristics = self.service.getCharacteristics()
            if Service_characteristics is not None:
                for characteristic in Service_characteristics:
                    if str(characteristic.uuid) == C_UUID:
                        CHARACT_ack = True
                        BoogieWD_Characteristic = characteristic
                        print('OK : Characteristic WatchDog Verified')
                    else:
                        print('ERROR : Characteristic WatchDog not found')
 
        except Exception as e:
            print('ERROR : Finding Characteristic UUID failed with exception : {}'.format(e))
        
        return BoogieWD_Characteristic       

# Verify WD identification of device
    def VerifyWD_ID(self, Service_UUID, Charact_UUID):
        self.GetServiceByUUID_WD(Service_UUID)
        self.GetCharacteristicsByUUID_WD(Charact_UUID)


# Read Characteristics for Watchdog Only (Unused fonction)
    def ReadCharacteristic_WD(self, Boogie_Characteristic_WD):
        try:
            WD_Characteristic_Data = Boogie_Characteristic_WD.read()
            print('My WD Characteristic value is : {}'.format(WD_Characteristic_Data))
        except Exception as e:
            print('Error in reading Watchdog Characteristic with : {}'.format(e))


# Get handle from service and data characteristic
    def SubscribeToIndication(self, ServiceUUID, DataCharacteristicUUID):
        self.DataHandle = None
        self.DataHDL = None
        DataUUID_OK = False
        try:
            self.Service = self.peripheral.getServiceByUUID(ServiceUUID)
        except Exception as e:
            print('ERROR : Subscribtion function failed to get service by UUID with exception : {}'.format(e))

        try:
            self.Characteristics = self.Service.getCharacteristics()
            if self.Characteristics is not None:
                for Characteristic in self.Characteristics:
#            print("Printing Char UUID : {} ".format(Characteristic))
                    if Characteristic.uuid == DataCharacteristicUUID:
                        self.DataHandle = Characteristic.getHandle()
                        self.DataHDL = self.DataHandle + 1
                        DataUUID_OK = True
                        print('OK : Subscribed to Indication')
                        break;

                    if DataUUID_OK == False:
                        print('ERROR : Data Characteristic UUID not found')
     
        except Exception as e:
            print('ERROR : Subscribtion function failed to get characteristic by UUID with exception : {}'.format(e))
        
        
    def InitializeDataTransfert(self, code):
        bytes1 = bytes(code, 'utf-8')
        try:
            self.peripheral.writeCharacteristic(self.DataHDL,bytes1)
            print('OK : Data transfert initialization Complete')
        except Exception as e:
            print('ERROR : Data transfert initialization failed with exception : {}'.format(e))


    def ReceivingData(self):
        try:
            self.peripheral.setDelegate(NotifyDelegate(self.DataHandle)) 
            while True:
                if  self.peripheral.waitForNotifications(2)== False:
                    print('OK : Data received :\n\r{}'.format(__BleDataInBuffer__))         
                    
                    break
#       writewithresponse()
    
        except Exception as e:
            print('ERROR : Setting delegate to receive data failed with exception : {}'.format(e))
   
           

    def writewithresponse(self,CharacteristicUUID, MessagetoSend):
        for Characteristic in self.Characteristics:
            if Characteristic.uuid == CharacteristicUUID:
                ResponseDataHandle = Characteristic.getHandle()
                try:
                    self.peripheral.writeCharacteristique(ResponseDataHandle, MessagetoSend, True)
                    print('Response received')
                except Exception as e:
                    print('TIMEOUT : No response received')
                

    def ConvertMessageLengthToBytes(self,message):
        MessageSize = len(message)
        print(MessageSize)

        if MessageSize > 0 and MessageSize < MaxLength:
            MsgByte =(MessageSize).to_bytes(4, byteorder='big')
            MsgByte1 = MsgByte[:1].hex() 
            MsgByte2 = MsgByte[1:2].hex()
            MsgByte3 = MsgByte[2:3].hex()
            MsgByte4 = MsgByte[3:4].hex()
            LengthByte = [MsgByte1, MsgByte2, MsgByte3, MsgByte4]
            print(LengthByte)
            
        else:
            LengthByte = 0
            print('Message Size is too big')
                            

    def WriteDataFile(self):
        
#        FileName = input("Enter file name you want to create/open with .extension : ") 
        FileName = "test_bmp.txt"
        try:
            f = open(FileName ,"a")
            f.write(str(__BleDataInBuffer__))
            f.write("\n\r")
            f.close()
            print("OK : Data written in File :", FileName)
        except Exception as e:
            print("Error in opening/closing File")

# print(LengthByte)

#    def SendData(self, message, DataDictionnary):
        # Connect to device, send length to characteristic and wait for changed v
            
                
