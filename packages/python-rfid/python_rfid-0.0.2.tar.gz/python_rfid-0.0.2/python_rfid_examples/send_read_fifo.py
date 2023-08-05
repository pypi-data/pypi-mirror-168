import python_rfid


def run():
    mfrc = python_rfid.mfrc522.MFRC522()
    mfrc.Init()
    mfrc.DumpVersion()

    mfrc.FlushFifoBuffer()
    data = [0x02, 0x14]
    mfrc.SendFifoData(data)
    print("Fifo data sent: {}".format(data))

    print("Fifo level: {}".format(
        mfrc.GetFifoLevel()
    ))
    
    recv = mfrc.ReadFifoData()
    print("Fifo data read: {}".format(recv.data))
