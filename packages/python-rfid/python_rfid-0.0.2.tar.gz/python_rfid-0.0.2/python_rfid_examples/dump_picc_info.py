"""
 * --------------------------------------------------------------------------------------------------------------------
 * Example sketch/program showing how to read data from a PICC to serial.
 * --------------------------------------------------------------------------------------------------------------------
 * This is a MFRC522 library example
 * 
 * Example sketch/program showing how to read data from a PICC (that is: a RFID Tag or Card) using a MFRC522 based RFID
 * Reader on a spidev SPI interface.
 * 
 * When the computer's SPI interface and the MFRC522 module are connected, run this script with python3. When
 * you present a PICC (that is: a RFID Tag or Card) at reading distance of the MFRC522 Reader/PCD, the terminal output
 * will show the ID/UID, type and any data blocks it can read. Note: you may see "Timeout in communication" messages
 * when removing the PICC from reading distance too early.
 * 
 * If your reader supports it, this sketch/program will read all the PICCs presented (that is: multiple tag reading).
 * So if you stack two or more PICCs on top of each other and present them to the reader, it will first output all
 * details of the first and then the next PICC. Note that this may take some time as all data blocks are dumped, so
 * keep the PICCs at reading distance until complete.
 * 
 * @license Released into the public domain.
"""

import python_rfid

GPIO_RESET_POWER_DOWN_PIN = 12 # PA12
GPIO_CHIP_SELECT_PIN = 13 # PC03

mfrc522 = python_rfid.mfrc522.MFRC522(
    #spi_bus = 1,
    #spi_device = 1,
    #spi_clock = 4000000,
    #gpio_chip = "/dev/gpiochip0",
    gpio_reset_power_down_pin = GPIO_RESET_POWER_DOWN_PIN,
    gpio_chip_select_pin = GPIO_CHIP_SELECT_PIN
)
pcd.Init()
time.sleep(0.05) # Optional delay. Some boards need more time after init to be ready
mfrc522.DumpVersion()

print("Scan PICC to see UID, SAK, type, and data blocks...")
print("Press CTRL+C to exit.")

picc_handler = python_rfid.picc_handler.PICC_Handler(mfrc522)

while True:
    if not picc_handler.IsNewCardPresent():
        uid = picc_handler.Select()
        picc_handler.DumpInfo(uid)
        picc_handler.HaltA(uid)
        break
    if not picc_handler.ReadCardSerial():
        break

    mfrc522.DumpToSerial(uid)
