from BLE import*



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
ble.ConnectToDevice(boogie)
print("------------------------------------------------------------------")


print("Test",n,": ID Verification")
n=n+1
#Find Watchdog service from Device and validate the UUID
S_UUID = "1a49d922-e3a9-4b00-9253-c4c72a1bcb5d"
ble.GetServiceByUUID_WD(S_UUID)
#Find Watchdog characteristic and validate the UUID
C_UUID =  "7895cecb-a923-4ce4-bc58-27e8ce6e00ea"
BoogieCharacteristic = ble.GetCharacteristicsByUUID_WD(C_UUID) 
print("------------------------------------------------------------------")


print("Test",n,": Subcription to Indication")
n=n+1
#Find Data Handle from data characteristic UUID. Prepare Handle+1 for writing
DataCharUUID = '04461336-088e-418e-b8aa-606bdcb8f300'
ServiceUUID = '67888895-69db-4168-8df4-9e12a10fa5b7'
ble.SubcribeToIndication(ServiceUUID, DataCharUUID)
print("------------------------------------------------------------------")


print("Test",n,": Data Transfert Initialization")
n=n+1
#Initialize Data transfert by writing 2 in bytes to the data characteristic
code = "\x02\x00"
ble.InitializeDataTransfert(code)
print("------------------------------------------------------------------")


print("Test",n,": Receiving Data")
n=n+1
#Enter a while loop to receive data. exit the while loop when timeout(10sec) is reach.
ble.ReceivingData()
print("------------------------------------------------------------------")





