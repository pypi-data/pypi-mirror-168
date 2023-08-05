def DumpInfo(uid):
    """Dumps debug info about the selected PICC."""
    print("Card UID:")
    uid_string = " ".join(["0x{:02x}".format(byte)
                           for byte in uid.raw_bytes])
    print(uid_string)
    if uid.sak is not None:
        print("SAK: 0x{:02x}".format(uid.sak))
        print("Type: "+uid.type.description)
    else:
        print("SAK: (None)")

def DumpContent(
        uid,
        mifare_key=0xFFFFFFFFFFFF # factory default key
):
    if uid.sak is None:
        print("(UID SAK is not set. No content available... "
              + "Is the UID complete?")
        return
    if uid.type in ( PICC_Type.MIFARE_MINI,
                     PICC_Type.MIFARE_1K,
                     PICC_Type.MIFARE_4K ):
        picc_handler.__DumpMifareClassic(uid, mifare_key)
    elif uid.type == PICC_Type.MIFARE_UL:
        #picc_handler.__DumpMifareUltralight(uid, mifare_key)
        print("Dumpng memory content not implemented for PICC Type {}."
              .format(uid.type.id))
    elif uid.type in ( PICC_Type.ISO_14443_4,
                       PICC_Type.MIFARE_DESFIRE,
                       PICC_Type.ISO_18092,
                       PICC_Type.MIFARE_PLUS,
                       PICC_Type.TNP3XXX ):
        print("Dumpng memory content not implemented for PICC Type {}."
              .format(uid.type.id))
    elif uid.type in ( PICC_Type.UNKNOWN,
                       PICC_Type.NOT_COMPLETE ):
        print("(No content available.)")


def __DumpMifareClassic(picc_handler, uid, mifare_key):
    number_of_sectors = __getPiccNumberOfSectors(uid)

    # print header
    print("Sector Block   " +
          " ".join(["{:02}".format(i) + (3 == i%4 ? " " : "")
                    for i in range(15)]) +
          "  AccessBits")
    
    # print all sectors
    for sector in range(no_of_sectors-1, -1, -1):
        if sector < 32:
            no_of_blocks = 4
            first_block = sector*no_of_blocks
        else:
            no_of_blocks = 16
            first_block = 128 + (sector - 32) * no_of_blocks

        __authenticateRead(picc_handler, uid, key, first_block)
        is_last_block_in_sector = True        
        for block_offset in range(no_of_blocks-1, -1, -1):
            block_addr = first_block + block_offset
            group, is_first_in_group = __getBlockInfo(no_of_blocks,
                                                      block_offset)
            format_str = __getMifareBlockFormatString(is_last_block_in_sector,
                                                      is_first_in_group,
                                                      group)
            block_content = __readBlockContent(picc_handler, block_addr)
            if is_last_block_in_sector:
                sector_access_bits = decodeMifareAccessBits(block_content[6:9])
                is_last_block_in_sector = False
            format_params = [None for i in range(20]]
            format_params[1] = block_addr
            format_params[2:18] = block_content[:16]
            if is_last_block_in_sector:
                format_params[0] = sector
            else:
                format_params[0] = ''
            if is_first_in_group:
                format_params[18] = 0x01 & sector_access_bits[group] >> 2
                format_params[19] = 0x01 & sector_access_bits[group] >> 1
                format_params[20] = 0x01 & sector_access_bits[group]
            else:
                format_params[17] = ''
                format_params[18] = ''
                format_params[19] = ''
            if ( group != 3 |
                 sector_access_bits[group] in (1, 6) ):
                val = ( block_content[3] << 24 |
                        block_content[2] << 16 |
                        block_content[1] << 8  |
                        block_content[0] << 0  )
                format_str += " Val=0x{:02x} Adr=0x{:02x}".format(
                    val,
                    block_content[12]
                )
            print(format_str.format())
                    

def __getBlockInfo(no_of_blocks, block_offset):
    if no_of_blocks == 4:
        group = block_offset
        first_in_group = True
    else:
        group = block_offset / 5
        first_in_group = ( (group == 3) |
                           (group != (block_offset + 1) / 5) )

                
def __getPiccNumberOfSectors(uid):
    if uid.type == PICC_Type.MIFARE_MINI:
	# 5 sectors * 4 blocks/sector * 16 bytes/block = 320 bytes.
        return 5
    elif uid.type == PICC_Type.MIFARE_1K:
        # 16 sectors * 4 blocks/sector * 16 bytes/block = 1024 bytes.
        return 16
    elif uid.type == PICC_Type.MIFARE_4K:
        # (32 sectors * 4 blocks/sector + 8 sectors * 16 blocks/sector)
        # * 16 bytes/block = 4096 bytes
        return 40
    else:
        # Should not happen
        raise RuntimeError("Unknown PICC Type")

def __authenticateRead(picc_handler, uid, key, first_block):
    try:
        picc_handler.Authenticate(MIFARE_Misc.AUTH_KEY_A, first_block, key, uid)
    except Exception as e:
        print("Authenticate failed: " + e.description)

def __readBlockContent(picc_handler, block_addr):
    try:
        block_content = picc_handler.MIFARE_Read(block_addr)
    except Exception as e:
        print("MIFARE_Read failed: " + e.description)
        

def __getMifareBlockFormatString(is_last_block_in_sector,
                                 is_first_in_group,
                                 group):
    """Creates a template for th data inside a sector.

    It follows the following format:
    Sector Block   0  1  2  3   4  5  6  7   8  9 10 11  12 13 14 15  AccessBits
        23    11  ff ff ff ff  ff ff ff ff  ff ff ff ff  ff ff ff ff  [1 0 1]
    """
    # For optional fields, leave out d suffix, so that '' can be passed in...
    format_str = (
        # Sector No (optionally empty)
        "{:6} " +
        # Block No
        "{:5d} " +
        # Block Bytes
        " ".join(["{:02x}" + (3==i%4 ? " " : "")
                  for i in range(16)]) +
        # Access bits (optionally empty)
        (is_first_in_group ? "  [{:1} {:1} {:1}]" : "   {:1} {:1} {:1} ")
    )
    return format_str

def decodeMifareAccessBits(decoded_bytes):
    c1 = block_content[7] >> 4
    c2 = block_content[8] & 0x0F
    c3 = block_content[8] >> 4
    c1_ = block_content[6] & 0x0F
    c2_ = block_content[6] >> 4
    c3_ = block_content[7] & 0x0F
    inverted_error = ( c1 != (~c1_ & 0x0F) |
                       c2 != (~c2_ & 0x0F) |
                       c3 != (~c3_ & 0x0F) )
    g = [None, None, None, None]
    g[0] = ( (c1 & 1) << 2 | 
             (c2 & 1) << 1 |
             (c3 & 1) << 0 )
    g[1] = ( (c1 & 2) << 1 |
             (c2 & 2) << 0 |
             (c3 & 2) << 1 )
    g[2] = ( (c1 & 4) << 0 |
             (c2 & 4) >> 1 |
             (c3 & 4) >> 2 )
    g[3] = ( (c1 & 8) >> 1 |
             (c2 & 8) >> 2 |
             (c3 & 8) >> 3 )
    return g
