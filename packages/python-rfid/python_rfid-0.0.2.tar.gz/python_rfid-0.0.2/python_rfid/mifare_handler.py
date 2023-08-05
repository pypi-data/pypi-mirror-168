# Defines common data structures for PICCs

import enum

import python_rfid.byte_utils
from python_rfid.picc_common import PICC_Type
from python_rfid.picc_handler import PICC_Handler

class MIFARE_Command(enum.Enum):
    """Command set of (different types of) MIFARE cards"""
    # The commands used for MIFARE Classic
    # (from http://www.mouser.com/ds/2/302/MF1S503x-89574.pdf, Section 9)
    #
    # Use PCD_MFAuthent to authenticate access to a sector,
    # then use these commands to read/write/modify the blocks on the sector.
    AUTH  = 0x0E      # Authenticate PCD as a reader
    READ       = 0x30 # Reads one 16 byte block from the authenticated
                         # ...sector of the PICC.
    WRITE      = 0xA0 # Writes one 16 byte block to the authenticated
                         # ...sector of the PICC.
    DECREMENT  = 0xC0 # Decrements the contents of a block and stores
                         # ...the result in the internal data register.
    INCREMENT  = 0xC1 # Increments the contents of a block and stores
                         # ...the result in the internal data register.
    RESTORE    = 0xC2 # Reads the contents of a block into the internal
                         # ...data register. 
    TRANSFER   = 0xB0 # Writes the contents of the internal data register
                         # ...to a block.
        
    # The commands used for MIFARE Ultralight
    # (from http://www.nxp.com/documents/data_sheet/MF0ICU1.pdf, Section 8.6)
    #
    # The MF_READ and MF_WRITE can also be used for MIFARE Ultralight.
    UL_WRITE      = 0xA2 # Writes one 4 byte page to the PICC.

class MIFARE_Misc(enum.Enum):
    """MIFARE constants that does not fit anywhere else."""
    AUTH_KEY_A = 0x60 # Authentication key type A
    AUTH_KEY_B = 0x61 # Authentication key type B
    MF_ACK= 0xA       # The MIFARE Classic uses a 4 bit ACK/NAK.
                      # ...Any other value than 0xA is NAK.
    KEY_SIZE = 6      # MIFARE key size

class MIFARE_Key:
    """Used for passing a MIFARE Crypto1 key."""

    @property
    def bytes(self):
        return self.__bytes

    def __init__(byte_vector = [0 for i in range(MIFARE_Misc.KEY_SIZE.value)]):
        self.__bytes = byte_vector

                      
class MIFARE_Handler(PICC_Handler):
    """Handles communication with MIFARE cards through a PCD."""

    def __init__(self, pcd):
        super().__init__(pcd)

    def SetAccessBits(g0, g1, g2, g3):
        """Calculates the bit pattern needed for the specified access bits. 

        In the [C1 C2 C3] tuples C1 is MSB (=4) and C3 is LSB (=1).
        """
        c1 = ( (g3 & 4) << 1 |
               (g2 & 4) << 0 |
               (g1 & 4) >> 1 |
               (g0 & 4) >> 2 )

        c2 = ( (g3 & 2) << 2 |
               (g2 & 2) << 1 |
               (g1 & 2) << 0 |
               (g0 & 2) >> 1 )
        
        c3 = ( (g3 & 1) << 3 |
               (g2 & 1) << 2 |
               (g1 & 1) << 1 |
               (g0 & 1) << 0 )

        access_bit_buffer = [None, None, None]
        access_bit_buffer[0] = (~c2 & 0xF) << 4 | (~c1 & 0xF)
        access_bit_buffer[1] = ( c1 & 0xF) << 4 | (~c3 & 0xF)
        access_bit_buffer[2] = ( c3 & 0xF) << 4 | ( c2 & 0xF)
        return access_bit_buffer

    def OpenUidBackdoor(log_errors):
        """Opens up UID sector on some Chinese cards.
        
        Note that you do not need to have selected the card through
        REQA or WUPA, this sequence works immediately when the card
        is in the reader vicinity. This means you can use this method
        even on "bricked" cards that your reader does not recognise 
        anymore (see UnbrickUidSector).
        
        Of course with non-bricked devices, you're free to select them
        before calling this function.
        """
        # Magic sequence:
        # > 50 00 57 CD (HALT + CRC)
        # > 40 (7 bits only)
        # < A (4 bits only)
        # > 43
        # < A (4 bits only)
        # Then you cann write to sector 0 without authenticating
    
        self.HaltA() # 50 00 57 CD
    
        try:
            response = self._pcd.Transceive([0x40],
                                            txLastBits=7,
                                            check_crc = False,
                                            doReturnData = True)
        except Exception as e:
            __log(log_errors,
                  ["Card did not respond to 0x40 after HALT command."
                   "Are you sure it is a UID changeable one?"])
            return False

        if len(response)!=1 or response[0] != 0x0A:
            __log(log_errors,
                  "Got bad response on backdoor 0x40 command.")
            return False;

        try:
            response = self._pcd.Transceive([0x43],
                                            txLastBits = 8,
                                            check_crc = False,
                                            doReturnData = True)
        except Exception as e:
            __log(log_errors,
                  "Error in communication at command 0x43, " +
                  "after successfully executing 0x40")
            return False
    
        if len(response) != 1 or response[0] != 0x0A:
            __log(log_errors,
                  "Got bad response on backdoor 0x43 command")
            return False

        return True;

    
    def SetUid(newUid, log_errors):
        """Set UID of the selected card.

        Reads entire block 0, including all manufacturer data, and overwrites
        that block with the new UID, a freshly calculated BCC, and the original
        manufacturer data.
        
        It assumes a default KEY A of 0xFFFFFFFFFFFF.
        Make sure to have selected the card before this function is called.
        """
        log = lambda err: logger.debug(err) if logError else None
        
        # UID + BCC byte can not be larger than 16 together
        if len(uid)>15:
            log("New UID size > 15 given.")
            return False
    
        # Authenticate for reading
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        try:
            self.PCD_Authenticate(MIFARE_Misc.AUTH_KEY_A,
                                  0x01, # Block address
                                  key,
                                  uid)
        except TimeoutError:
            # Wake the card up again if sleeping
            #byte atqa_answer[2];
            #byte atqa_size = 2;
            #PICC_WakeupA(atqa_answer, &atqa_size);
            
            if (not self.IsNewCardPresent()) | (not self.ReadCardSerial()):
                log("No card was previously selected, and none are available. Failed to set UID.")
                return False

        try:
            self.PCD_Authenticate(MIFARE_Misc.AUTH_KEY_A,
                                  0x01, # block_addr
                                  key,
                                  uid)
        except Exception as e:
            log("Failed to authenticate to card for reading, could not set UID.")
            return False
            
        try:
            block0 = self.Read(0x00)
        except Exception as e:
            log("Failed to read block 0. Are you sure your Key A for block 0 is 0xFFFFFFFFFFFF")
            return False
    
        # Write new UID to the data we just read, and calculate BCC byte
        bcc = 0x00
        block0[0:len(uid)] = uid
        block0[len(uid)] = byte_utils.xor(uid)

        # Stop encrypted traffic so we can send raw bytes
        self.PCD_StopCrypto1();
    
        # Activate UID backdoor
        if not self.OpenUidBackdoor(log_errors):
            log("Activating the UID backdoor failed.")
            return False
    
        # Write modified block 0 back to card
        try:
            self.Write(0x00, # block_addr
                              block0,
                              16)
        except Exception as e:
            log("Write() failed")
            return False
    
        # Wake the card up again
        atqa_answer = self.WakeupA()
        return True

    def UnbrickUidSector(log_errors):
        """Resets entire sector 0 to zeroes, so the card can be read again."""
        self.OpenUidBackdoor(log_errors);

        block0 = [0x00 for i in range(16)]
        block0[0:4] = [0x01, 0x02, 0x03, 0x04]
        block0[4:7] = [0x04, 0x08, 0x04]

        try:
            self.Write(0x00, #block_addr
                              block0)
        except Exception as e:
            log("Write() failed")
            return False;
        
        return True;

    def SetValue(block_addr, value):
        """Helper routine to write a specific value into a Value Block.
        
        Only for MIFARE Classic and only for blocks in "value block" mode, that
        is: with access bits [C1 C2 C3] = [110] or [001]. The sector containing
        the block must be authenticated before calling this function. 
        """
        buf = [None for i in range(16)]
        buf[0] = value & 0xFF
        buf[1] = (value & 0xFF00) >> 8
        buf[2] = (value & 0xFF0000) >> 16
        buf[3] = (value & 0xFF000000) >> 24
        
        buf[4:8] = [invertByte(buf[i]) for i in range(4)]
        buf[8:12] = buf[0:4]
        
        buf[12] = block_addr
        buf[13] = invertByte(block_addr)
        buf[14:16] = buf[12:14]

        self.Write(block_addr, buf)

    def Ultralight_Write(page, data):
        """Writes a 4 byte page to the active MIFARE Ultralight PICC.

        Args:
            page (Integer): The page (2-15) to write to.
            data (list): The (four) bytes to be written.
        """
        cmd = [MIFARE_Command.UL_WRITE.value, page] + data
        self.Transceive(cmd)

    def Write(block_addr, data):
        """Writes 4-16 bytes to the active PICC.
        
        For MIFARE Classic the sector containing the block
        must be authenticated before calling this function.
        
        For MIFARE Ultralight the operation is called "COMPATIBILITY WRITE".
        Even though 16 bytes are transferred to the Ultralight PICC, 
        only the least significant 4 bytes (bytes 0 to 3)
        are written to the specified address. It is recommended to set
        the remaining bytes 04h to 0Fh to all logic 0.
        """
        byte_utils.assertByte(block_addr)
        byte_utils.assertBytes(data)
        if len(data)<16:
            data += [0 for i in range(16-len(data))]
            
        cmd = [MIFARE_Command.WRITE.value, block_addr]
        self.Transceive(cmd)
        self.Transceive(data)


    def Read(block_addr):
        """Reads 16 bytes (+ 2 bytes CRC_A) from the active PICC.
        
        For MIFARE Classic the sector containing the block must be 
        authenticated before calling this function.

        For MIFARE Ultralight only addresses 0x00 to 0x0F are decoded.
        The MF0ICU1 returns a NAK for higher addresses.

        The MF0ICU1 responds to the READ command by sending 16 bytes
        starting from the page address defined by the command argument.
        For example, if block_addr is 0x03 then pages 0x03, 0x04, 0x05, 0x06 
        are returned.

        A roll-back is implemented: 
        If block_addr is 0Eh, then the contents of pages 0x0E, 0x0F, 0x00
        and 0x01 are returned.
        """
        byte_utils.assertByte(block_addr)
        data = [MIFARE_Command.READ, block_addr]
        data += self.CalculateCrcBytes(data)
        return self.Transceive(
            data,
            check_crc=True,
            do_return_data=True
        )


    # Functions for communicating with MIFARE PICCs
    def Authenticate(cmd, block_addr, key, uid):
        """Executes the MFRC522 MFAuthent command.

        This command manages MIFARE authentication to enable a secure
        communication to any MIFARE Mini, MIFARE 1K and MIFARE 4K card.

        The authentication is described in 
        - the MFRC522 datasheet section 10.3.1.9 and 
        - http://www.nxp.com/documents/data_sheet/MF1S503x.pdf section 10.1.
        
        For use with MIFARE Classic PICCs.
        
        The PICC must be selected - ie in state ACTIVE(*) - before calling
        this function. Remember to call StopCrypto1() after communicating
        with the authenticated PICC, otherwise no new communications can start.

        All keys are set to 0xFFFFFFFFFFFF at chip delivery.
        """
        byte_utils.assertByte(block_addr)
        assert cmd in [MIFARE_Misc.AUTH_KEY_A, MIFARE_Misc.AUTH_KEY_B], \
                       ("command must be one of PICC_Command.MF_AUTH_KEY_A " +
                        "or PICC_Command.MF_AUTH_KEY_B." )

        # Reminder: The last 4 uid bytes never contain a cascade tag...
        data = [cmd.value, block_addr] + key.bytes + uid.raw_bytes[-4:]
        self.CommunicateWithPICC(
            PCD_Command.PCD_MFAuthent,
            PCD_IrqBits.Idle,
            data
        )

    def Restore(block_addr):
        """MIFARE Restore copies the value of the addressed block into a volatile memory.

        For MIFARE Classic only. The sector containing the block must be authenticated before calling this function.
        Only for blocks in "value block" mode, ie with access bits [C1 C2 C3] = [110] or [001].
        Use Transfer() to store the result in a block.
        """
        # The datasheet describes Restore as a two step operation, but does not explain what data to transfer in step 2.
        # Doing only a single step does not work, so I chose to transfer 0L in step two.
        self.__TwoStepHelper(MIFARE_Command.RESTORE, block_addr, 0);

    def Decrement(block_addr, delta):
        """Subtracts the delta from the value of the addressed block, and stores the result in a volatile memory.
        
        For MIFARE Classic only. The sector containing the block must be authenticated before calling this function.
        Only for blocks in "value block" mode, ie with access bits [C1 C2 C3] = [110] or [001].
        Use Transfer() to store the result in a block.
        """
        self.__TwoStepHelper(MIFARE_Command.DECREMENT, block_addr, delta)

    def Increment(block_addr, delta):
        """MIFARE Increment adds the delta to the value of the addressed block, and stores the result in a volatile memory.

        For MIFARE Classic only. The sector containing the block must be authenticated before calling this function.
        Only for blocks in "value block" mode, ie with access bits [C1 C2 C3] = [110] or [001].
        Use Transfer() to store the result in a block.
        """
        self.__TwoStepHelper(MIFARE_Command.INCREMENT, block_addr, delta)


    def Transfer(block_addr):
        """MIFARE Transfer writes the value stored in the volatile memory into one MIFARE Classic block.

        For MIFARE Classic only. The sector containing the block must be authenticated before calling this function.
        Only for blocks in "value block" mode, ie with access bits [C1 C2 C3] = [110] or [001].
        """
        cmd_buffer = [None, None]
        
        # Tell the PICC we want to transfer the result into block block_addr.
        cmd_buffer[0] = MIFARE_Command.TRANSFER
        cmd_buffer[1] = block_addr
        self.Transceive(cmd_buffer, 2)


    def GetValue(block_addr, value):
        """Helper routine to read the current value from a Value Block.
        
        Only for MIFARE Classic and only for blocks in "value block" mode, that
        is: with access bits [C1 C2 C3] = [110] or [001]. The sector containing
        the block must be authenticated before calling this function. 
        """
        buf = self.Read(block_addr)
        return (buf[3] << 24) | (buf[2] << 16) | (buf[1] << 8) | buf[0]
        
    def SendCommand(self, command, data=[]):
        """Sends a command to the active MIFARE Card."""
        seq = [command.value] + data
        result = self.Transceive(seq)
        return result
        
    def Transceive(data, acceptTimeout = False):
        """Wrapper for MIFARE protocol communication.

        Adds CRC_A, executes the Transceive command and 
        checks that the response is MF_ACK or a timeout.
        """
        cmd_buffer = [None for i in range(18)] # We need room for 16 bytes data and 2 bytes CRC_A.
    
        if len(data)>16:
            raise Exception("Invalid input")
    
        cmd_buffer[:len(data)] = data
        cmd_buffer[len(data):len(data)+2] = self.CalculateCrcBytes(data)
        try:
            result = self.CommunicateWithPICC(PCD_Command.Transceive,
                                             (PCD_IrqBits.Rx, PCD_IrqBits.Idle),
                                             cmd_buffer,
                                             txLastBits=8,
                                             doReturnData=True);
        except TimeoutError as err:
            if not acceptTimeout:
                raise err

        if ( result.valid_bits_last_byte != 4
             or MIFARE_Misc.MF_ACK != result.data[0] & 0x0F ):
            raise Exception("NACK")

        return result

    
    def __TwoStepHelper(self, command, block_addr, data):
        """Helper function for the two-step MIFARE Classic protocol operations Decrement, Increment and Restore."""

        cmd_buffer = [None, None]
        
        # Step 1: Tell the PICC the command and block address
        cmd_buffer[0] = command
        cmd_buffer[1] = block_addr
        self.Transceive(cmd_buffer, 2)
        
        # Step 2: Transfer the data
        self.Transceive(data, 4, True) # Accept timeout as success


    def PCD_NTAG216_AUTH(password, pACK):
        """Authenticate with a NTAG216.

        Only for NTAG216. First implemented by Gargantuanman.
        """
        # TODO: Fix cmd_buffer length and rxlength. They really should match.
        #       (Better still, rxlength should not even be necessary.)

        cmd_buffer = [None for i in range(18)] # We need room for 16 bytes data and 2 bytes CRC_A.
    
        cmd_buffer[0] = 0x1B # Authentication command
        cmd_buffer[:4] = password
        # FIXME Shouldn't this (next line) be the first 4 bytes?
        cmd_buffer[4:6] = self.CalculateCrcBytes(cmd_buffer[:5]) 
    
        return self.CommunicateWithPICC(PCD_Command.Transceive,
                                        (PCD_IrqBits.Rx, PCD_IrqBits.Idle),
                                        cmd_buffer,
                                        # backLen = 5, # rxlength (?)
                                        txLastBits=0,
                                        doReturnData = True)

        
    def PICC_DumpMifareClassicToSerial(uid, piccType, key):
        pass

    def PICC_DumpMifareClassicSectorToSerial(uid, key, sector):
        pass

    def PICC_DumpMifareUltralightToSerial():
        pass

def __log(log_errors, msg):
    if log_errors:
        for err in log_errors:
            logger.debug(err)
