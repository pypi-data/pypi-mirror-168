import enum

class PCD_Error(enum.Enum):
    Protocol    = 0x01
    Parity      = 0x02
    Crc         = 0x04
    Collision   = 0x08
    BufferOvfl  = 0x10
    #           = 0x20 # reserved
    Temperature = 0x40
    BufferWr    = 0x80
    

class TimeoutError(Exception):
    """Raised when a timeout occurs."""
    def __init__(self, msg="Timeout occured."):
        super().__init__(msg)

class CollisionError(Exception):
    """A collision occured during SELECT/ANTICOLLISION."""
    def __init__(self,
                 msg="Collision detected during SELECT/ANTICOLLISION loop."):
        super().__init__(msg)

class TemperatureError(Exception):
    """The temperature of the PCD is over a given threashold."""
    def __init__(self, msg="Antenna drivers switched off due to overheating."):
        super().__init__(msg)

class BufferOverflowError(Exception):
    """The FIFO buffer of the PCD is full, but someone tries to write to it."""
    def __init__(self, msg="The FIFO buffer of the PCD is already full."):
        super().__init__(msg)

class CrcError(Exception):
    """The RxModeReg register’s RxCRCEn bit is set and the CRC calculation fails

    Automatically cleared to logic 0 during receiver start-up phase.
    """
    def __init__(self, msg="CRC error detected!"):
        super().__init__(msg)

class AtqaError(Exception):
    """Thrown when no ATQA was received or the ATQA had a wrong format."""
    def __init__(self, msg="Unexpected ATQA bit length received."):
        super().__init__(msg)
