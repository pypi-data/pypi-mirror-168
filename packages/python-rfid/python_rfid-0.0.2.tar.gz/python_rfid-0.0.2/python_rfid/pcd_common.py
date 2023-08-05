# Defines common data structures for PCDs.




class FifoBuffer:
    """A data stream received from the FifoBuffer on the PCD 

    This is usually data received from a PICC).
    """
        
    @property
    def data(self):
        return self.__data
    """Data received from the PICC."""
    
    @property
    def valid_bits(self):
        """Number of valid bits."""
        return self.__valid_bits

    @property
    def valid_bits_last_byte(self):
        """The valid bits in the last byte of data. 

        If the buffer length is 0, valid_bits_last_byte is defined to be 8!
        """
        bits = self.valid_bits % 8
        if bits == 0:
            bits = 8
        return bits

    def __init__(self, data=[], valid_bits_last_byte=8):
        if valid_bits_last_byte == 0:
            raise RuntimeError("Valid bits in the last byte should be in (0,8]. 0 must be converted to 8.")
        self.__valid_bits = 8*(len(data)-1)+valid_bits_last_byte
        self.__data = data

