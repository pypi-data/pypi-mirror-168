# Defines common data structures for PICCs

import enum

import python_rfid.byte_utils
from python_rfid.errors import PCD_Error
from python_rfid.picc_common import PICC_Type, Uid
from python_rfid.errors import *
from python_rfid.pcd_common import FifoBuffer
from python_rfid.mfrc522 import PCD_Register

class PICC_Command(enum.Enum):
    """Command set of standard proximity cards."""
            
    REQA    = 0x26 # REQuest command Type A. (7 bit frame)
                   # ...Invites PICCs in State IDLE to go to READY
                   # ...and prepare for anticollision or selection.
    WUPA    = 0x52 # Wake-up command Type A. (7 bit frame)
                   # Invites PICCs in state IDLE and HALT to go to READY(+)
                   # and prepare for anticolllision or selection.
    HLTA    = 0x50 # HALT command Type A.
                   # Instructs an ACTIVE PICC to go to state HALT.
    RATS    = 0xE0 # REQuest command for Answer to Reset
    SEL_CL0 = 0x93 # Anti collision/select, Cascade level 1
    SEL_CL1 = 0x95 # Anti collision/select, Cascade level 2
    SEL_CL2 = 0x97 # Anti collision/select, Cascade level 3

class PICC_Handler:
    """Implements algorithms to communicte with standard proximity cards.

    The following PICC_Commands are implemented:
    - HaltA (HLTA)
    - WakeUpA (WUPA)
    - RequestA (REQA)
    - Select (combines SEL_CL0, SEL_CL1 and SEL_CL2)

    For communicating with PICCs, a PCD is needed.
    """

    def __init__(self, pcd):
        """Expects a pcd device for communicating with PICCs."""
        self._pcd = pcd

    def HaltA(self):
        seq = [PICC_Command.HLTA.value, 0]
        seq += list(self._pcd.CalculateCrcBytes(seq))
        try:
            self._pcd.Transceive(seq)
            raise RuntimeError("Receiving data from PICC is not expected! " +
                               "Not acknowledged!")
        except TimeoutError:
            pass

    def RequestA(self):
        """Transmits a REQuest command, Type A.
        
        Invites PICCs in state IDLE to go to READY and prepare for
        anticollision or selection. 7bit frame.
        
        Beware: When two PICCs are in the field at the same time I often
        get STATUS_TIMEOUT - probably due to bad antenna design.
        
        Returns:
            list(int): The answer to the request
        """
        return self.__RequestOrWakeUp(PICC_Command.REQA)

    def WakeUpA(self):
        """Transmits a Wake-up command, Type A. 

        Invites PICCs in state IDLE and HALT to go to READY(+) and prepare
        for anticollision or selection. 7bit frame.

        Beware: When two PICCs are in the field at the same time I often get
        STATUS_TIMEOUT - probably due to bad antenna design.

        Returns:
            list(int): The answer to the request.
        """
        return self.__RequestOrWakeUp(PICC_Command.WUPA)


    def Select(self, uid = Uid()):
        """Transmits SELECT/ANTICOLLISION commands to select a single PICC.

        Before calling this function the PICCs must be placed in the READY(*)
        state by calling RequestA() or WakeupA().
        
        On success:
        - The chosen PICC is in state ACTIVE(*) and all other PICCs have
          returned to state IDLE/HALT. (Figure 7 of the ISO/IEC 14443-3 draft.)
        - The UID size and value of the chosen PICC is returned as an instance
          of Uid class along with its SAK.

        A PICC UID consists of 4, 7 or 10 bytes. Only 4 bytes can be specified
        in a SELECT command, so for the longer UIDs two or three iterations
        are used:

        UID size  Number of UID bytes  Cascade levels  Example of PICC
        =======================================================================
        single    4                    1               MIFARE Classic
        double    7                    2               MIFARE Ultralight
        triple    10                   3               Currently not available?
        
        Returns:
            Uid of the card
        """

        # TODO If uid has already known bytes, perform all previous select statements.
        
        while not uid.is_complete:
            # At least one ANTICOLLISION step is always needed.
            # Appends at least one bit to uid.
            uid = self.__PerformAnticollisionStep(uid)
            while len(uid.raw_bytes) not in (4, 8, 12) or \
                  uid.valid_bits_last_byte != 8:
                uid = self.__PerformAnticollisionStep(uid)

            buf = self.__CreateBufferForSelectAndAnticollision(
                uid,
                for_select=True
            )
            sak_buffer = self._pcd.Transceive(
                buf,
                check_crc = False
            )
            self._pcd.CheckForErrors(PCD_Error.Collision)
            uid.setSakByte(sak_buffer.data[0])
            # TODO Check CRC(=sak[1:3]) of sak

        return uid
        
    # FIXME what happens if a uid is given that is not present?            

    def __CreateBufferForSelectAndAnticollision(self, uid, for_select):
        # Description of buffer structure:
        # Byte 0: SEL (indicates cascade level)
        # Byte 1: NVB (number of valid bits of whole buffer
        #              high nibble: complete bytes, low nibble: extra bits)  
        # Byte 2: UID-data or CascadeTag
        # Byte 3: UID-data
        # Byte 4: UID-data
        # Byte 5: UID-data
        # Byte 6: BCC (block check character - XOR of bytes 2-5)
        # Byte 7: CRC_A
        # Byte 8: CRC_A
        #
        # The BCC and CRC_A are only transmitted if we know all the UID bits
        # of the current Cascade Level.
        #
        # Description of bytes 2-5:
        # (Section 6.5.4 of the ISO/IEC 14443-3 draft:
        #  UID contents and cascade levels)
        #
        # UID size    Cascade level    Byte2    Byte3    Byte4    Byte5
        # ========    =============    =====    =====    =====    =====
        # 4 bytes     1                uid0     uid1     uid2     uid3
        # 7 bytes     1                CT       uid0     uid1     uid2
        #             2                uid3     uid4     uid5     uid6
        # 10 bytes    1                CT       uid0     uid1     uid2
        #             2                CT       uid3     uid4     uid5
        #             3                uid6     uid7     uid8     uid9

        assert (not for_select) | uid.is_cascade_complete, \
            ( "A select can only be done if all bytes " +
              "of the current cascade level are known.")            
        
        buf = [None, None]
        if uid.valid_bits < 4*8 or \
           uid.valid_bits == 4*8 and for_select:
            buf[0] = PICC_Command.SEL_CL0.value
            buf += uid.raw_bytes
        elif uid.valid_bits < 8*8 or \
             uid.valid_bits == 8*8 and for_select:
            buf[0] = PICC_Command.SEL_CL1.value
            buf += uid.raw_bytes[4:]
        elif uid.valid_bits < 12*8 or \
             uid.valid_bits == 12*8 and for_select:
            buf[0] = PICC_Command.SEL_CL2.value
            buf += uid.raw_bytes[8:]
        else:
            raise RuntimeError("Unknown cascade level!")

        if for_select:
            buf[1] = 0x70 # Indicate select command
            buf += [None, None, None]
            buf[6] = python_rfid.byte_utils.xor(buf[2:6])
            buf[7:9] = self._pcd.CalculateCrcBytes(buf[:7])
        else: # anticollision
            # buf[1] contains the whole number of valid bits, including
            # SEL byte and NVB byte
            buf[1] = ((2 + int(uid.valid_bits / 8)) << 4) + uid.valid_bits % 8

        return buf

    def __RequestOrWakeUp(self, command):
        """Transmits REQA or WUPA commands.

        Beware: When two PICCs are in the field at the same time I often get 
        STATUS_TIMEOUT - probably due to bad antenna design.

        Returns:
            list(int): The answer to the request.
        """
        self._pcd.SetClearCollisionBits(do_clear=False)
        
        atqa = self._pcd.Transceive([command.value], tx_last_bits=7)
        self._pcd.CheckForErrors(PCD_Error.Collision)
        
        if len(atqa.data) != 2 or atqa.valid_bits_last_byte != 8:
            raise AtqaError("Unexpected ATQA bit length received.")
        return atqa

    
    def __PerformAnticollisionStep(self, uid = Uid()):
        """Transmits ANTICOLLISION commands to select a single PICC.

        Before calling this function, the PICCs must be placed in the READY(+) 
        state by calling PICC_RequestA() or PICC_WakeupA().
        """
        buf = self.__CreateBufferForSelectAndAnticollision(uid,
                                                           for_select=False)
        known_uid = FifoBuffer(buf[2:], uid.valid_bits_last_byte)
        result = self._pcd.Transceive(
            buf,
            rx_align = uid.valid_bits_last_byte % 8,
            tx_last_bits = uid.valid_bits_last_byte,
            prefix_bytes = known_uid,
            check_crc = False
        )
        try:
            self._pcd.CheckForErrors(PCD_Error.Collision)
            if result.data[4] != python_rfid.byte_utils.xor(result.data[0:4]):
                raise RuntimeError("BCC does not match UID!")
            return Uid(result.data[0:4], result.valid_bits_last_byte)
        except CollisionError as err:
            position = self._pcd.GetCollisionPosition()
            if position <= known_uid.valid_bits:
                raise RuntimeError("Internal error: " +
                                   "collision at position <= valid bits.")
            
            uid_full_bytes = result.data[:(position-1)/8]
            uid_collision_byte = result.data[1+(position-1)/8]
            # choose the uid with byte set
            uid_collision_byte |= 0x80  >> (7 - (position-1) % 8)
            valid_bits_last_byte = position % 8
            if valid_bits_last_byte == 0:
                valid_bits_last_byte = 8
            return Uid(data = uid_full_bytes + [uid_collision_byte],
                       valid_bits_last_byte = position%8)

        
    def IsNewCardPresent(self):
        # FIXME: Are the next lines really needed?
        # Reset baud rates
        #self._pcd.UpdateRegister(PCD_Register.TxMode, 0x00)
        #self._pcd.UpdateRegister(PCD_Register.RxMode, 0x00)
        # Reset PCD_Register.ModWidth
        #self._pcd.UpdateRegister(PCD_Register.ModWidth, 0x26)
        #self.RequestA()        
        try:
            self.RequestA()
            return True
        except CollisionError:
            logger.debug("collision occured")
            return True
        except AtqaError:
            logger.debug("atqa error: no card present?")
        except TimeoutError:
            logger.debug("timeout error: no card present?")
        except Exception as e:
            raise e
        return False

