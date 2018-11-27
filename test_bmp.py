from BLE import*

#---------------------------------------------------------------------------------------------------
#Var.Globale

DataDict = {"WD_ServiceUUID" : "1a49d922-e3a9-4b00-9253-c4c72a1bcb5d","WD_CharactUUID" : "7895cecb-a923-4ce4-bc58-27e8ce6e00ea","Data_ServiceUUID" : "67888895-69db-4168-8df4-9e12a10fa5b7" , "DataOUT_CharactUUID" : "04461336-088e-418e-b8aa-606bdcb8f300", "Length_CharactUUID" : "713a155c-5ae2-4604-9ec4-078ad627926e"  ,"DataIN_CharactUUID" : "e7a87ad7-9ce0-40d0-896f-7fbc3d10d9ff", "Key_Init" : "\x02\x00"}

#---------------------------------------------------------------------------------------------------


print("-----------------")
print("Python : " + platform.python_version())
print("DEMO : TEST BMP")
print("-----------------")

print("")

print("-----------------")
print("Connection au Blackbox")
print("-----------------")


ble = BleDevice()
ble.Scan(1)
boogie = ble.FindBoogie()
ble.ConnectToDevice(boogie)
ble.SubscribeToIndication(DataDict["Data_ServiceUUID"], DataDict["DataOUT_CharactUUID"])
#Initialize Data transfert by writing 2 in bytes to the data characteristic
ble.InitializeDataTransfert(DataDict["Key_Init"])


print("")
print("-----------------")
print("Reception des donnes")
print("-----------------")


#Reception 1 paquet
#Enter a while loop to receive data. exit the while loop when timeout(10sec) is reach.
ble.ReceivingData()

FileName = "test_bmp.txt"

ble.WriteDataFile(FileName)


print("End")
