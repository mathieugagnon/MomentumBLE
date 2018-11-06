from BLE import*



print("---------------")
print("Python : " + platform.python_version())
#print("Bluepy : " + bluepy.__version__)
print("---------------")


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

## Read WD Characteristic value and confirm the value
#ble.ReadCharacteristic_WD(BoogieCharacteristic) 
#ServiceUUID = '67888895-69db-4168-8df4-9e12a10fa5b7'
#RdyCharUUID = '713a155c-5ae2-4604-9ec4-078ad627926e'
#ble.ReadyToReceiveData(ServiceUUID, RdyCharUUID)


#Find Data Handle from data characteristic UUID. Prepare Handle+1 for writing
DataCharUUID = '04461336-088e-418e-b8aa-606bdcb8f300'
ServiceUUID = '67888894-69db-4168-8df4-9e12a10fa5b7'
ble.SubcribeToIndication(ServiceUUID, DataCharUUID)

#Initialize Data transfert by writing 2 in bytes to the data characteristic
code = "\x02\x00"
ble.InitializeDataTransfert(code)

#Enter a while loop to receive data. exit the while loop when timeout(10sec) is reach.
ble.ReceivingData()



