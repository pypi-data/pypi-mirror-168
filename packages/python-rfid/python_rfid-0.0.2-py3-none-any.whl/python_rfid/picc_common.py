from enum import Enum

from python_rfid import byte_utils

class PICC_Type(Enum):
    """PICC types we can detect."""

    @property
    def description(self):
        return self.value

    @property
    def id(self):
        return self.name
        
    ISO_14443_4    = "PICC compliant with ISO/IEC 14443-4"
    ISO_18092      = "PICC compliant with ISO/IEC 18092 (NFC)",
    MIFARE_MINI    = "MIFARE Mini, 320 bytes",
    MIFARE_1K      = "MIFARE 1KB",
    MIFARE_4K      = "MIFARE 4KB",
    MIFARE_UL      = "MIFARE Ultralight or Ultralight C",
    MIFARE_PLUS    = "MIFARE Plus",
    MIFARE_DESFIRE = "MIFARE DESFire",
    TNP3XXX        = "MIFARE TNP3XXX",
    NOT_COMPLETE   = "(SAK indicates UID is not complete)"
    UNKNOWN        = "Unknown PICC type"

class Uid:
    """Wrapping the UID of a PICC.

    A UID can have different lengths: 4, 7 or 10 bytes.

    During communication with the PICC (in particular during the anticollision
    loop), a UID is always considered to be 4, 8 or 12 bytes long, where the
    extra bytes are additional cascade tags, which indicate whether or not a
    UID is complete. That is why these cascade tags are included in the property
    raw_bytes.
    """
    
    CASCADE_TAG = 0x88

    @property
    def is_complete(self):
        """True, iff the Uid is complete.

        A UID may be incomplete during the ANTICOLLISION/SELECT algorithm.
        """
        return 8*(4+3*self.cascade_level) == self.valid_bits

    @property
    def is_cascade_complete(self):
        """True, iff all bytes of the current cascade level are known."""
        return (
            self.valid_bits_last_byte==8
            and len(self.raw_bytes) in (4, 8, 12)
        )
    
    @property
    def cascade_level(self):
        """Returns the cascade level of the (partial) UID.

        If the anticollision loop has not finished yet, this is only a lower
        estimate of the true cascade level.
        """
        return sum([self.CASCADE_TAG==b for b in self.raw_bytes])
            

    @property
    def raw_bytes(self):
        """A list of UID bytes inclusive of cascade tags. 

        May be incomplete (see #is_complete and #valid_bits)."""
        return self.__raw_bytes


    @property
    def valid_bits(self):
        """The number of valid bits.

        During anticollision, only part of the id is valid. In particular, the
        last byte may be only partially valid. In this case, #valid bits shows
        how many bits of all bytes are valid (including cascade tags).
        """
        return self.__valid_bits

    @property
    def valid_bits_last_byte(self):
        """The number of valid bits in the last byte."""
        num = self.valid_bits % 8
        if num == 0:
            num = 8
        return num
        
    @property
    def sak(self):
        """The Select Acknowledge Byte obtained after successful selection."""
        return self.__sak

    @property
    def type(self):
        """The type of the PICC. If sak is None: PICC_Type.NOT_COMPLETE."""
        return self.__inferTypeFromSak(self)
        
    def __init__(self, raw_bytes=[], valid_bits_last_byte=0, sak=None):
        self.__raw_bytes = raw_bytes
        if 0<len(raw_bytes):
            self.__valid_bits = 8*(len(raw_bytes)-1)+valid_bits_last_byte
        else:
            self.__valid_bits = 0
        self.__sak = sak

    def __inferTypeFromSak(self):
        if self.sak is not None:
            PICC_Sak_To_Types = {
                0x04: PICC_Type.NOT_COMPLETE,
                0x09: PICC_Type.MIFARE_MINI,
                0x08: PICC_Type.MIFARE_1K,
                0x18: PICC_Type.MIFARE_4K,
                0x00: PICC_Type.MIFARE_UL,
                0x10: PICC_Type.MIFARE_PLUS,
                0x11: PICC_Type.MIFARE_PLUS,
                0x01: PICC_Type.TNP3XXX,
                0x20: PICC_Type.ISO_14443_4,
                0x40: PICC_Type.ISO_18092
            }
            if (self.sak & 0x7F) in PICC_Sak_To_Types:
                # fixme: use complete sak?
                return PICC_Sak_To_Types[self.sak & 0x7F]
            else:
                return PICC_Type.UNKNOWN
        else:
            return PICC_Type.NOT_COMPLETE

    def setSakByte(self, sak):
        """Sets the SAK byte.

        This can only be done once and only if the UID is complete.
        """
        byte_utils.assertByte(sak)
        if not self.is_complete:
            self.__sak=sak
    
