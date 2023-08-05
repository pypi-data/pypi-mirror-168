import python_rfid
import time

def run():
    pcd = python_rfid.mfrc522.MFRC522()
    pcd.Init()
    pcd.DumpInfo()
    picc_hdl = python_rfid.picc_handler.PICC_Handler(pcd)
    while True:
        if picc_hdl.IsNewCardPresent():
            print("Found new card!")
            try:
                uid = picc_hdl.Select()
                print(uid.raw_bytes)
            except:
                print("Select failed...")
        else:
            pass
        time.sleep(0.5)

