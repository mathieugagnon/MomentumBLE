from BLE import*

DataDict = {"WD_ServiceUUID" : "1a49d922-e3a9-4b00-9253-c4c72a1bcb5d","WD_CharactUUID" : "7895cecb-a923-4ce4-bc58-27e8ce6e00ea","Data_ServiceUUID" : "67888895-69db-4168-8df4-9e12a10fa5b7" , "DataOUT_CharactUUID" : "04461336-088e-418e-b8aa-606bdcb8f300", "Length_CharactUUID" : "713a155c-5ae2-4604-9ec4-078ad627926e"  ,"DataIN_CharactUUID" : "e7a87ad7-9ce0-40d0-896f-7fbc3d10d9ff", "Key_Init" : "\x02\x00"}

print("---------------")
print("Python : " + platform.python_version())
#print("Bluepy : " + bluepy.__version__)
print("---------------")

n = 1

# Main Code -----------------------------------------------------------
#print("Test",n, ": Creation d'un objet BLEdevice")
#n=n+1

ble = BleDevice()
print("------------------------------------------------------------------")



print("Test",n, ": Detection of Boogie companion")
n=n+1
ble.Scan(5.0)
boogie = ble.FindBoogie()
print("------------------------------------------------------------------")



print("Test",n, ": Connection to Boogie ")
n=n+1
#Find device named boogie in device list
DeviceStatus = ble.ConnectToDevice(boogie)
print("------------------------------------------------------------------")



print("Test",n,": ID Verification")
n=n+1
#Find Watchdog service from Device and validate the UUID
#ble.GetServiceByUUID_WD(DataDict["WD_ServiceUUID"])
#Find Watchdog characteristic and validate the UUID
#BoogieCharacteristic = ble.GetCharacteristicsByUUID_WD(DataDict["WD_CharactUUID"]) 
ble.VerifyWD_ID(DataDict["WD_ServiceUUID"],DataDict["WD_CharactUUID"])
print("------------------------------------------------------------------")



print("Test",n,": Subcription to Indication")
n=n+1
#Find Data Handle from data characteristic UUID. Prepare Handle+1 for writing
ble.SubcribeToIndication(DataDict["Data_ServiceUUID"], DataDict["DataOUT_CharactUUID"])
print("------------------------------------------------------------------")



print("Test",n,": Data Transfert Initialization")
n=n+1
#Initialize Data transfert by writing 2 in bytes to the data characteristic
ble.InitializeDataTransfert(DataDict["Key_Init"])
print("------------------------------------------------------------------")



print("Test",n,": Receiving Data")
n=n+1
#Enter a while loop to receive data. exit the while loop when timeout(10sec) is reach.
ble.ReceivingData()
print("------------------------------------------------------------------")



print("Test",n,": Sending Data")
n=n+1
message = ''
#ble.SendData(message, DataDict)
print("------------------------------------------------------------------")



print("------------------------------------------------------------------")
i = 256
Message = bytearray(i) 
ble.ConvertMessageLengthToBytes(Message)
print("------------------------------------------------------------------")



print("Test",n,": Disconnection from device")
n=n+1
ble.DisconnectFromDevice(boogie)
print("------------------------------------------------------------------")


print("END OF TEST")


