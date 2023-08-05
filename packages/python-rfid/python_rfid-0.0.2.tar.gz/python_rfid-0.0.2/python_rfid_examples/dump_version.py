import python_rfid

def run():
    pcd = python_rfid.mfrc522.MFRC522()
    pcd.Init()
    pcd.DumpVersion()

