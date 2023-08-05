import operator

def xor(byte_list):
    """Calculates XOR of all bytes in byte_list.
    
    Args:
        byteList (list): An iterable of bytes.
    
    Returns:
        The byte formed by applying xor to all bytes in byte_list.
    """
    bcc = 0x00
    for byte in byte_list:
        bcc = operator.xor(byte, bcc)
    return bcc

def updateBits(n, value, update):
    """Updates the n most significant bits of original with those in update.

    Args:
        n (int): The amount of bits to take from original.
        original (int): The original byte.
        update (int): The new byte.
    
    Returns:
        An int representing the byte with the first n most significant bits
        taken from update the the last (8-n) least significant bits from
        value.
    """
    assertByte(original, varname="original")
    assertByte(update, varname="update")
    if n<0 or n>8:
        raise ValueError("n must be between 0 and 8!")

    bits_from_update = (0xFF << rx_align) & 0xFF
    return (value & ~bits_from_update) | (updated_value & bits_from_update)


def assertBytes(bvector, varname=None):
    """Checks whether each entry of bvector is a byte or not, ie. in [0,255].
    
    Args:
        bvector (list): A list of ints to be checked.
        varname (str): A meaningful variable name.
    
    Raises:
        AssertionError: An AssertionError is raised if i is not a byte. If 
            varname is not None, the description of the error has a meaningful
            explanation.
    """
    for byte in bvector:
        assertByte(byte, varname)


def assertByte(i, varname=None):
    """Checks whether i is a byte or not, ie. i is in [0,255].

    Args:
        i (int): The int to be checked.
        varname (str): A meaningful variable name used for the description of
            a possibly raised AssertionError.

    Raises:
        AssertionError: An AssertionError is raised if i is not a byte. If
            varname is not None, the description of the error has a meaningful
            explanation.
    """
    if i<0 or i>255:
        if varname is None:
            err="Expected a byte, but an int (out of range) was given."
        else:
            err= ( "Argument " + varname +
                   " must be a byte (ie. an in between 0 and 255)." )
        raise AssertionError(err)
