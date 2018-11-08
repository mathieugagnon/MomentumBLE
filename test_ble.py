from BLE import*



print("---------------")
print("Python : " + platform.python_version())
#print("Bluepy : " + bluepy.__version__)
print("---------------")


# Main Code -----------------------------------------------------------
print("test 1")
ble = BleDevice()

print("test 2")
ble.Scan(5.0)

print("test 3")
boogie = ble.FindBoogie()

print("test 4")
#Find device named boogie in device list
ble.ConnectToDevice(boogie)

print("test 5")
#Find Watchdog service from Device and validate the UUID
S_UUID = "1a49d922-e3a9-4b00-9253-c4c72a1bcb5d"
ble.GetServiceByUUID_WD(S_UUID)

print("test 6")
#Find Watchdog characteristic and validate the UUID
C_UUID =  "7895cecb-a923-4ce4-bc58-27e8ce6e00ea"
BoogieCharacteristic= ble.GetCharacteristicsByUUID_WD(C_UUID) 

print("test 7")
#Find Data Handle from data characteristic UUID. Prepare Handle+1 for writing
DataCharUUID = '04461336-088e-418e-b8aa-606bdcb8f300'
ServiceUUID = '67888895-69db-4168-8df4-9e12a10fa5b7'
ble.SubcribeToIndication(ServiceUUID, DataCharUUID)

print("test 8")
#Initialize Data transfert by writing 2 in bytes to the data characteristic
code = "\x02\x00"
ble.InitializeDataTransfert(code)

print("test 9")
#Enter a while loop to receive data. exit the while loop when timeout(10sec) is reach.
ble.ReceivingData()


#Char_WithResponseUUID = ""
#ble.writewithresponse(Char_WithResponseUUID)

