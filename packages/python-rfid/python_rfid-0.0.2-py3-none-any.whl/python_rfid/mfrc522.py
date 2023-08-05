"""
This module implements a proximity coupling device (PCD).

In order to be accepted by a PICC_Handler, a PCD must implement the following
methods:
- CommunicateWithPICC
- Transceive
- CheckForErrors, ie. check for a PCD_Error.Collision
- GetCollisionPosition
- CalculateCrcBytes
- SetClearCollisionBits

In order to be accepted by a MIFARE_Handler, it needs to - in addition -
implement the following methods:
- [...]
"""

import logging
logger = logging.getLogger(__name__)

from enum import Enum
import itertools
import time

import gpiod
import spidev

from python_rfid.errors import *
from python_rfid.pcd_common import FifoBuffer
import python_rfid.byte_utils as byte_utils
import python_rfid.self_test_data


class PCD_CrcPresetValues(Enum):
    """Defines preset for the PCD_Command.CalcCrc calculation."""
    ZERO   = 0x00  # 0x0000 preset
    LOW    = 0x01  # 0x6363 preset
    MEDIUM = 0x10  # 0xA671 preset
    HIGH   = 0x11  # 0xFFFF preset

class PCD_Register(Enum):
    """Constants for accessing PCD Registers.
        
    Described in section 9 of the datasheet 
    currently found at https://www.nxp.com/docs/en/data-sheet/MFRC522.pdf
    or in the docs folder.
    """
    # Page 0: Command and status
    #         0x00      # reserved for future use
    Command = 0x01 << 1 # starts and stops command execution
    ComIEn  = 0x02 << 1 # enable and disable interrupt request control bits
    DivIEn  = 0x03 << 1 # enable and disable interrupt request control bits
    ComIRq  = 0x04 << 1 # interrupt request bits
    DivIRq  = 0x05 << 1 # interrupt request bits
    Error   = 0x06 << 1 # error bits showing the error status of the last command executed
    Status1    = 0x07 << 1 # communication status bits
    Status2    = 0x08 << 1 # receiver and transmitter status bits
    FifoData   = 0x09 << 1 # input and output of 64 byte FIFO buffer
    FifoLevel  = 0x0A << 1 # number of bytes stored in the FIFO buffer
    WaterLevel = 0x0B << 1 # level for FIFO underflow and overflow warning
    Control    = 0x0C << 1 # miscellaneous control registers
    BitFraming = 0x0D << 1 # adjustments for bit-oriented frames
    Coll       = 0x0E << 1 # bit position of the first bit-collision detected
                           # ...on the RF interface
    #          = 0x0F << 1 # reserved for future use

    # Page 1: Command
    #           = 0x10 << 1 # reserved
    Mode        = 0x11 << 1 # defines general modes for transmitting
                            # ...and receiving
    TxMode      = 0x12 << 1 # defines transmission data rate and framing
    RxMode      = 0x13 << 1 # defines reception data rate and framing
    TxControl   = 0x14 << 1 # controls the logical behavior
                            # ...of the antenna driver pins TX1 and TX2
    TxASK       = 0x15 << 1 # controls the transmission modulation
    TxSel       = 0x16 << 1 # selects the internal sources
                            # ...for the antenna driver
    RxSel       = 0x17 << 1 # selects the internal receiver settings
    RxThreshold = 0x18 << 1 # selects thresholds for the bit decoder
    Demod       = 0x19 << 1 # defines demodulator settings
    #           = 0x1A << 1 # reserved
    #           = 0x1B << 1 # reserved
    MfTx        = 0x1C << 1 # controls some MIFARE communication
                            # ...transmit parameters
    MfRx        = 0x1D << 1 # ...and receive parameters
    #           = 0x1E << 1 # reserved
    SerialSpeed = 0x1F << 1 # selects the speed of the serial UART interface

    # Page 2: Configuration
    #              = 0x20 << 1 # reserved
    CrcResultH     = 0x21 << 1 # The MSB of the result of the CRC calculation.
    CrcResultL     = 0x22 << 1 # The LSB of the result of the CRC calculation.
    #              = 0x23 << 1 # reserved
    ModWidth       = 0x24 << 1 # controls the ModWidth
    #              = 0x25 << 1 # reserved
    RFCfg          = 0x26 << 1 # configures the receiver gain
    GsN            = 0x27 << 1 # selects the conductance of the antenna driver
                               # ...pins TX1 and TX2 for mudulation
    CWGsP          = 0x28 << 1 # defines the conductance of the p-driver output
                               # ...during periods of NO modulation
    ModGsP         = 0x29 << 1 # ...during periods of modulation
    TMode          = 0x2A << 1 # settings for the internal timer: 0x08=TAuto
    TPrescaler     = 0x2B << 1 # The lower 8 bits of the TPrescaler value.
                               # ...The 4 high bits are in TMode.
    TReloadH       = 0x2C << 1 # 16-bit timer reload value (MSB)
    TReloadL       = 0x2D << 1 # ... and LSB
    TCounterValueH = 0x2E << 1 # 16-bit timer value (MSB)
    TCounterValueL = 0x2F << 1 # ... and LSB

    # Page 3: Test Registers
    #            = 0x30 << 1 # reserved
    TestSel1     = 0x31 << 1 # general test signal configuration
    TestSel2     = 0x32 << 1 # general test signal configuration
    TestPinEn    = 0x33 << 1 # enables pin output driver on pins D1 to D7
    TestPinValue = 0x34 << 1 # defines the values for D1 to D7
                             # ...when it is used as an I/O bus
    TestBus      = 0x35 << 1 # shows the status of the internal test bus
    AutoTest     = 0x36 << 1 # controls the digital self-test
    Version      = 0x37 << 1 # shows the software version
    AnalogTest   = 0x38 << 1 # controls the pins AUX1 and AUX2
    TestDAC1     = 0x39 << 1 # defines the test value for TestDAC1
    TestDAC2     = 0x3A << 1 # defines the test value for TestDAC2
    #            = 0x3C << 1 # reserved for production tests
    #            = 0x3D << 1 # reserved for production tests
    #            = 0x3E << 1 # reserved for production tests
    #            = 0x3F << 1 # reserved for production tests


class PCD_IrqBits(Enum):
    # Div
    Crc = 0x04
    MfinAct = 0x10
    # Com
    Timer = 0x01
    Err = 0x02
    LoAlert = 0x04
    HiAlert = 0x08
    Idle = 0x10
    Rx = 0x20
    Tx = 0x40

class PCD_Command(Enum):
    """MFRC522 commands. Described in chapter 10 of the datasheet."""

    Idle       = 0x00 # no action, cancels currend command execution
    Mem        = 0x01 # stores 25 bytes into the internal buffer
    GenRandId  = 0x02 # generates a 10-byte random ID number
    CalcCrc    = 0x03 # activates the CRC coprocessor or performs a self-test
    Transmit   = 0x04 # transmits data from the FIFO buffer
    NoCmd      = 0x07 # no command change, can be used to modify the Command
                      # ...register bits without affecting the command,
                      # ...for example, the PowerDown bit
    Receive    = 0x08 # activates the receiver circuits
    Transceive = 0x0C # transmits data from FIFO buffer to antenna and
                      # ...automatically activates the receiver after
                      # ...transmission
    SoftReset  = 0x0F # resets the MFRC522

    
class PCD_RxGain(Enum):
    """MFRC522 RxGain[2:0] defines the receiver's signal voltage gain factor.

    Described in 9.3.3.6 / table 98 of the datasheet 
    currently found at https://www.nxp.com/docs/en/data-sheet/MFRC522.pdf
    or in the docs folder.
    """
    RxGain_18dB   = 0x00 << 4 # 18dB, minimum
    RxGain_23dB   = 0x01 << 4 # 23 dB
    RxGain_18dB_2 = 0x02 << 4 # 18 dB ...it seems 010b is a duplicate for 000b
    RxGain_23dB_2 = 0x03 << 4 # 23 dB ...it seems 011b is a duplicate for 001b
    RxGain_33dB   = 0x04 << 4 # 33 dB, average, and typical default
    RxGain_38dB   = 0x05 << 4 # 38 dB
    RxGain_43dB   = 0x06 << 4 # 43 dB
    RxGain_48dB   = 0x07 << 4 # 48 dB, maximum
    # some convenience levels
    RxGain_min    = 0x00 << 4 # 18 dB, minimum
    RxGain_avg    = 0x04 << 4 # 33 dB, average
    RxGain_max    = 0x07 << 4 # 48 dB, maximum

class MFRC522:
    
    FIFO_SIZE = 64

    _gpio_chip_select_pin = None
    _chip_select_line = None
    _gpio_reset_power_down_pin = None
    _reset_line = None
    _gpio_irq_pin = None
    _irq_line = None
    
    _spidev = None
    _gpiod = None
        
    def __init__(self,
                 spi_bus = 0,
                 spi_device = 0,
                 spi_clock = 4000000,
                 gpio_chip = "/dev/gpiochip0",
                 gpio_reset_power_down_pin = 2, # PA2, alt: PA12=12
                 gpio_chip_select_pin = 67, # PC03, alt PA13=13
                 gpio_irq_pin = 68 # PC04
                 ):
        logger.debug("(spi_bus, spi_device)=({}, {})".format(spi_bus, spi_device))
        logger.debug("(rst_pin, cs_pin, irq_pin)=({}, {}, {})".format(
            gpio_reset_power_down_pin,
            gpio_chip_select_pin,
            gpio_irq_pin
        ))
        self._spidev = spidev.SpiDev()
        self._spidev.open(spi_bus, spi_device)
        self._spidev.max_speed_hz = spi_clock
        self._spidev.lsbfirst = False
        self._spidev.mode = 0b00
        # self._spidev.cshigh = False

        self._gpiod = gpiod.chip(gpio_chip)
        self._gpio_reset_power_down_pin = gpio_reset_power_down_pin
        self._gpio_chip_select_pin = gpio_chip_select_pin
        self._gpio_irq_pin = gpio_irq_pin
        

    def WriteRegister(self, reg, values):
        """Sends data to a PCD register.
        
        Parameters:
        reg (PCD_Register): The register to write to.
        values (list): A list of bytes to be sent to the device.
        """
        assertRegister(reg, "reg")
        byte_utils.assertBytes(values)
        seq = [maskWrite(reg.value)] + list(values)
        self._chip_select_line.set_value(0)
        self._spidev.xfer2(seq)
        self._chip_select_line.set_value(1)

    def ReadRegister(self, reg, mask=0xFF):
        """Reads n values from register reg.

        Parameters:
        reg (PCD_Register): The register address to read from.
        mask (int): A bit mask of the bits to read.
        
        Returns:
        int: The byte, which were received.
        """
        assertRegister(reg, "reg")
        byte_utils.assertByte(mask)
        seq = [maskRead(reg.value), 0]
        self._chip_select_line.set_value(0)
        values = self._spidev.xfer2(seq)
        self._chip_select_line.set_value(1)
        return values[1] & mask # First byte does not carry any information.

    def ResetBaudRates(self):
        """Resets Tx and Rx baud rates from the PCD device."""
        self.UpdateRegister(PCD_Register.TxMode, 0x00)
        self.UpdateRegister(PCD_Register.RxMode, 0x00)

    def SetClearCollisionBits(self, do_clear=True):
        """If set, all received bits after a collision will be cleared.
        
        Only used during bitwise anticollision at 106 kBd, otherwise always on.

        Args:
            do_clear (bool): If True, clearing is on.
        """
        if do_clear:
            self.UpdateRegister(PCD_Register.Coll, 1, 0x80)
        else:
            self.UpdateRegister(PCD_Register.Coll, 0, 0x80)            
        
    def ResetModWidth(self):
        """Resets modulation width of the PCD device."""
        self.UpdateRegister(PCD_Register.ModWidth, 0x26)

    def SetTimer(self, mu, count):
        """Sets the timer.
        The PCD timer counts down from TReloadVal to 0. The time for one
        decrement step is the timer_delay, so that in total the timeout occurs
        after (TReloadVal+1) * timer_delay seconds.

        The timer delay has theoretical bounds of [0.22, 604] microseconds and
        can also be set using SetTimerDelay.

        The TReloadVal has bounds of [1, 655535] and can also be set using
        SetTimerSteps.
        """
        self.SetTimerDelay(mu)
        self.SetTimerSteps(count)

    def SetTimerDelay(self, mu):
        """Sets the timer delay of the PCD timer. (See SetTimer.)

        Args:
            mu (int): The delay time in microseconds.
        """
        # f_timer = 13.56 MHz / (2*TPreScaler+1)
        prescaler = int((mu * 13.56 - 1) / 2)
        if prescaler > 0xFFF:
            raise ValueError("Timer value is too big!" +
                             " Max 604 microseconds allowed!")
        if prescaler == 0:
            raise ValueError("Timer value is too small!" +
                             " Min 0.22 microseconds allowed!")

        pre_high = prescaler >> 8
        pre_low = prescaler & 0xFF
        self.UpdateRegister(PCD_Register.TMode, pre_high, 0x0F)
        self.UpdateRegister(PCD_Register.TPrescaler, pre_low)

    def SetTimerSteps(self, count):
        """Sets the value for TReloadVal. (See. SetTimer)."""
        assert (count>=0 & count <= 65535), \
            "The timer count must be in [0,65535]"
        reload_low = count & 0xFF
        reload_high = count >> 8
        self.UpdateRegister(PCD_Register.TReloadL, reload_low)
        self.UpdateRegister(PCD_Register.TReloadH, reload_high)

    def Force100AskModulation(self, off=False):
        if off:
            self.UpdateRegister(PCD_Register.TxASK, 0x00)
        else:
            self.UpdateRegister(PCD_Register.TxASK, 0x40)

    def SetCrcPresetValue(self, val):
        assert type(val)==PCD_CrcPresetValues, \
            "val must be an instance of PCD_CrcPresetValues"
        self.UpdateRegister(PCD_Register.Mode, val.value, 0x03)
    
    def SetAutoTimer(self):
        """Sets PCD timer to auto mode, ie. start timer after transmission

        Timer starts immediately after transmitting data in any communication
        mode and at any speed.
        """
        self.UpdateRegister(PCD_Register.TMode, 0x80)        
        
    def SetRegisterBitMask(self, reg, mask):
        """Apply mask to the bits in register reg.
        
        Parameters:
        reg (PCD_Register): 
            The register, which will be updated.
        mask (int): 
            A bit mask, which is applied to register reg
            via bitwise-or.
        """
        assertRegister(reg, "reg")
        byte_utils.assertByte(mask)
        tmp = self.ReadRegister(reg)
        self.UpdateRegister(reg, tmp | mask);

    def UpdateRegister(self, reg, value, mask=0xFF):
        """Updates selected bits from a register.
        
        With mask=0xFF the whole register is overwritten, so this function is
        an alternative to WriteRegister for registers, which only support
        writing single bytes.
        
        Args:
            reg (PCD_Register): The PCD_Register to update.
            mask (int): A bit mask indicating, which bits should be updated.
            value (int): The new value of the indicated bits.
        """
        byte_utils.assertByte(mask)
        byte_utils.assertByte(value)
        assert type(reg)==PCD_Register, "reg must be a PCD_Register!"
        if mask==0xFF:
            new_value=value
        else:
            #logger.debug("Reading old register value of {}".format(reg))
            current_value = self.ReadRegister(reg)
            new_value = (current_value & ~mask) | (value & mask)
        self.WriteRegister(reg, [new_value])

    def ClearRegisterBitMask(self, reg, mask):
        """Clears all bits which are not set in mask.

        Parameters:
        reg (PCD_Register): The register, which will be updated.
        mask (byte): The bit mask, which will be applied.
        """
        assertRegister(reg, "reg")
        byte_utils.assertByte(mask)
        tmp = self.ReadRegister(reg)
        self.UpdateRegister(reg, tmp & (~mask))

    def CalculateCrcInteger(self, data, timeout_ms = 90):
        """Calculates the CRC of a list of bytes returning one two-byte int.

        Parameters:
        data (list): A list of bytes.
        timeout_ms (int): Timeout in ms.

        Returns:
        A 2-tuple of the high and low bits of CRC; high bit first.
        """
        crc_high, crc_low = self.CalculateCrcBytes(data, timeout_ms)
        return crc_low + (crc_high << 8)

    def CalculateCrcBytes(self, data, timeout_ms = 90):
        """Calculates the CRC of a list of bytes returning two separate ints.

        Parameters:
        data (list): A list of bytes.
        timeout_ms (int): Timeout in ms.

        Returns:
        A 2-tuple of the high and low bits of CRC; high bit first.
        """
        self.SendCommand(PCD_Command.Idle)
        self.ClearCrcIrq()
        self.FlushFifoBuffer()
        self.WriteRegister(PCD_Register.FifoData, data)
        self.SendCommand(PCD_Command.CalcCrc);
        self.WaitForDivIRqBit(PCD_IrqBits.Crc, timeout_ms)
        self.SendCommand(PCD_Command.Idle)
            
        crc_low = self.ReadRegister(PCD_Register.CrcResultL)
        crc_high = self.ReadRegister(PCD_Register.CrcResultH)
        return [crc_low, crc_high]

    
    def CheckForErrors(self, error_list = None):
        """Checks if any error bit is set and if so, raises an error.
        
        The bits in PCD_Register.Error are checked from low to high
        significancy.
        """
        if error_list is None:
            mask=0xFF
        elif hasattr(error_list, '__iter__'):
            mask = sum([e.value for e in error_list])
        else:
            mask = error_list.value
        errors = self.ReadRegister(PCD_Register.Error) & mask
        if 0x01 & errors:
            raise RuntimeError("ProtocolError")
        elif 0x02 & errors:
            raise RuntimeError("ParityError")
        elif 0x04 & errors:
            raise CrcError()
        elif 0x08 & errors:
            raise CollisionError()
        elif 0x10 & errors:
            raise BufferOverflowError()
        elif 0x20 & errors:
            raise RuntimeError("reserved")
        elif 0x40 & errors:
            raise TemperatureError()
        elif 0x80 & errors:
            raise RuntimeError("WrErr")
        
    
    def ClearComIRqReg(self, mask = 0x7F):
        """Clears Com IRQ Register bits.
        
        Args:
            mask (int): 
                A bit-mask of the PCD_Register.ComIRq bits to be cleared. Bits
                indicated with a logic 1 will be cleared. The MSB will be 
                checked and must be set to 0.
        """
        byte_utils.assertByte(mask)
        assert not (mask & 0x80), "Highest bit may not be set."
        self.UpdateRegister(PCD_Register.ComIRq, mask)

    def ClearDivIRqReg(self, mask = 0x7F):
        """Clears the Div IRQ Register bits.

        Parameters:
        mask (int): The bits to be cleared.
        """
        byte_utils.assertByte(mask)
        assert not (mask & 0x80), "Highest bit may not be set."
        self.UpdateRegister(PCD_Register.DivIRq, mask)

    def ClearCrcIrq(self):
        """Clears the CRC IRQ Register bit."""
        self.ClearDivIRqReg(0x04)
            
    def SetComIRqReg(self, mask):
        """Sets IRQ Register bits.
        
        Args:
            mask (int): A bit-mask of the PCD_Register.ComIRq bits to be set.
                Bits indicated with a logic 1 will be set. The MSB will be 
                checked and must be set to 1.
        """
        byte_utils.assertByte(mask)
        assert not (mask & 0x80), "Highest bit may not be set."
        self.UpdateRegister(PCD_Register.ComIRq, 0x80 | mask)

    def SendCommand(self, command):
        """Sends a command to the PCD.
        
        Args:
            command (PCD_Command): A valid PCD command.

        """
        assert type(command)==PCD_Command, "Not a PCD_Command."
        self.UpdateRegister(PCD_Register.Command, command.value)
        
    def FlushFifoBuffer(self):
        """Flush the FIFO buffer of the PCD device.

        Immediately clears the internal FIFO buffer's read and write pointer
        and PCD_Register.Error register's BufferOvfl bit.
        """
        self.UpdateRegister(PCD_Register.FifoLevel, 0x80)

    def SendFifoData(self, data):
        """Sends data to the FIFO buffer.

        Args:
            data (list): A list of integers (interpreted as bytes).
        """
        byte_utils.assertBytes(data)
        self.WriteRegister(PCD_Register.FifoData, data)

    def SetBitFraming(self, rx_align, tx_last_bits):
        """Sets the bit framing of the device."""
        assert (tx_last_bits>0 & tx_last_bits<9), \
            "tx_last_bits must be in [1,8]"
        assert (rx_align>=0 & rx_align < 8), \
            "rx_align must be in [0,7]"
        if tx_last_bits == 8:
            tx_last_bits = 0
        bit_framing = (rx_align << 4) + tx_last_bits
        self.UpdateRegister(PCD_Register.BitFraming, bit_framing)

    def GetBitFraming(self):
        """Reads the current bit framing settings from the device.

        Returns:
            A 2-tuple consisting of [rx_align, tx_last_bits]
        """
        value = self.ReadRegister(PCD_Register.BitFraming)
        rx_align = value & 0x70 >> 4
        tx_last_bits = value & 0x70
        if tx_last_bits == 0:
            tx_last_bits = 8
        return rx_align, tx_last_bits

    def GetRxLastBits(self):
        """Reads the valid bits of the last byte in fifo buffer."""
        valid_bits = self.ReadRegister(PCD_Register.Control) & 0x07
        if valid_bits==0:
            valid_bits=8
        return valid_bits
                
    def StartTransceive(self):
        """Starts a transceive command.

        Starting the transceive command is done by setting the StartSend bit 
        of the PCD_Register.BitFraming."""
        self.SetRegisterBitMask(PCD_Register.BitFraming, 0x80)

    def WaitForComIRqBit(self, bits, timeout_ms = 50):
        """Waits until a bit in PCD_Register.ComIRq is set. 

        Args:
            timeout_ms (int): Timeout in milliseconds.

        Raises:
            TimeoutError: Raised when timeout_ms is reached.
        """
        self.WaitForIrqBit(PCD_Register.ComIRq, bits, timeout_ms)

    def WaitForDivIRqBit(self, bits, timeout_ms = 50):
        """Waits until a bit in DivIRq is set. 

        Args:
            timeout_ms (int): Timeout in milliseconds.

        Raises:
            TimeoutError: Raised when timeout_ms is reached.
        """
        self.WaitForIrqBit(PCD_Register.DivIRq, bits, timeout_ms)

    def WaitForIrqBit(self, register, bits, timeout_ms = 50):
        """Waits for PCD_Register.ComIRq or PCD_Register.DivIRq bits. 
        
        Args:
            register (PCD_Register): 
                Either PCD_Register.ComIRq or PCD_Register.DivIRq
            bits (list(PCD_IrqBits):
                An iterable of PCD_IrqBits.
            timeout_ms (int): Timeout in milliseconds.
        
        Raises:
            TimeoutError: Raised when timeout_ms is reached.
        """
        assert register in (PCD_Register.ComIRq, PCD_Register.DivIRq), \
            "register must be one of PCD_Register.ComIRq, PCD_Register.DIvIrq"
        # TODO asserts
        if hasattr(bits, '__iter__'):
            mask = sum([b.value for b in bits])
        else:
            mask = bits.value
        byte_utils.assertByte(mask)
        deadline = time.time() + timeout_ms/1000.
        while time.time() < deadline:
            state = self.ReadRegister(register)
            if state & mask:
                return
            elif state & 0x01:
                break
        raise TimeoutError("IRq bit not set!")

    def GetFifoLevel(self):
        """Reads the level of the FIFO buffer on the device."""
        return self.ReadRegister(PCD_Register.FifoLevel)

    def ReadFifoData(self, n=None, prefix_bytes=FifoBuffer()):
        """Reads data from the FIFO buffer.
        
        Args:
            n (int): 
                Number of bytes to read. If n==0, the whole buffer is read.
            prefix_bytes (FifoBuffer): 
                A list of bytes to prepend to the data. rx_align is read from
                the PCD and taken into account, ie. the last (8-rx_align) bits
                of the last byte in this list are replaced by the last
                (8-rx_align) bits of the first byte that is received. It is
                checked that the number valid bits in the last byte of
                prefix_bytes match the rx_align value read from the PCD.
        """
        if n is None:
            n = self.GetFifoLevel()
        
        if n>0:
            seq = n * [maskRead(PCD_Register.FifoData.value)] + [0]
            self._chip_select_line.set_value(0)            
            received_data = self._spidev.xfer2(seq)
            self._chip_select_line.set_value(1)            
            received_data = received_data[1:] # first byte doesn't carry data

            valid_bits_last_byte = self.GetRxLastBits()
            if valid_bits_last_byte == 0:
                valid_bits_last_byte = 8

            rx_align = prefix_bytes.valid_bits_last_byte % 8
                
            # |b0|b1|b2|b3|b4|b5|b6|b7|, rx_align=4
            #    => 4 preceding bits => valid_bits_last_byte>=4
            if ( (len(received_data) == 1) &
                 (valid_bits_last_byte < rx_align) ):
                raise RuntimeError("Unexpected!" +
                                   " How can a single received byte have less" +
                                   " valid bits than rx_align?!")
            
            if rx_align == 0:
                data = prefix_bytes.data + received_data
            else:
                last_byte = prefix_bytes.data[-1]
                updated_byte = byte_utils.updateBits(rx_align,
                                                     last_byte,
                                                     received_data[0])
                data = ( prefix_bytes.data[:-1] +
                         [updated_byte] +
                         received_data[1:] )
                
            return FifoBuffer(data, valid_bits_last_byte)
        else:
            return prefix_bytes
    
    # Functions for manipulating the MFRC522
    def Init(self):
        hard_reset = False
        # No need for manipulating _gpio_chip_select_pin (output_mode + HIGH)?

        config = gpiod.line_request()
        config.consumer = "MFRC522"
        config.request_type = gpiod.line_request.DIRECTION_OUTPUT
        self._chip_select_line = self._gpiod.get_line(
            self._gpio_chip_select_pin
        )
        self._chip_select_line.request(config)
        self._chip_select_line.set_value(1) # disable slave
        
        if self._gpio_reset_power_down_pin != None:
            config = gpiod.line_request()
            config.consumer = "MFRC522"
            config.request_type = gpiod.line_request.DIRECTION_OUTPUT
            self._reset_line = self._gpiod.get_line(
                self._gpio_reset_power_down_pin
            )
            self._reset_line.request(config)
            self._reset_line.set_value(0)
            time.sleep(0.01)
            self._reset_line.set_value(1)
            time.sleep(0.05)
            logger.debug("Hard reset successful...")
            hard_reset = True

        if self._gpio_irq_pin is not None:
            config = gpiod.line_request()
            config.consumer = "MFRC522"
            config.request_type = gpiod.line_request.DIRECTION_INPUT
            self._irq_line = self._gpiod.get_line(
                self._gpio_irq_pin
            )
            self._irq_line.request(config)

        if not hard_reset:
            logger.debug("Performing soft reset...")
            self.Reset()

        logger.debug("Starting Init()")
        self.ResetBaudRates()
        self.ResetModWidth()

        self.SetAutoTimer()
        self.SetTimer(25, 1000) # 25 milliseconds
                                    # = (25 microseconds / count  * 1000 counts)
        self.Force100AskModulation() # Force 100% ASK modulation
        self.SetCrcPresetValue(PCD_CrcPresetValues.LOW)
        self.AntennaOn()
        logger.debug("Init() done")


    def Reset(self):
        self.SendCommand(PCD_Command.SoftReset)
        time.sleep(0.05)
        for _ in range(4):
            if not self.ReadRegister(PCD_Register.Command, 1<<4):
                # This bit indicates that the soft reset finished
                # and the device is back up.
                return
            else:
                time.sleep(0.05)
        raise TimeoutError()


    def AntennaOn(self):
        """Turns the antenna on. After soft reset, the antenna is disabled."""
        self.UpdateRegister(PCD_Register.TxControl, 0x03, 0x03)

    def AntennaOff(self):
        self.ClearRegisterBitMask(PCD_Register.TxControl, 0x03)

    def GetAntennaGain(self):
        """Reads the antenna gain from the PCD device.
        
        Returns:
            An instance of PCD_RxGain.
        """
        return PCD_RxGain(
            self.ReadRegister(PCD_Register.RFCfg, 0x07<<4) >> 4
        )

    def SetAntennaGain(self, gain):
        assert type(gain)==PCD_RxGain, "gain must be a PCD_RxGain."
        if self.GetAntennaGain() != gain:
            self.ClearRegisterBitMask(PCD_Register.RFCfg, 0x07<<4)
            self.UpdateRegister(PCD_Register.RFCfg, gain.value)

    def PerformSelfTest(self):
        """Returns True/False"""

        version = self.ReadRegister(PCD_Register.Version)
        ref_data = self_test_data.getReferenceDataForVersion(version)
        
        self.Reset()

        self.FlushFifoBuffer()

        self.WriteRegister(PCD_Register.FifoData,
                               [0x00 for i in range(25)])
        self.SendCommand(PCD_Command.Mem)
        
        self.UpdateRegister(PCD_Register.AutoTest, 0x09)
        # TODO implement config command?
        
        self.SendFifoData([0x00])
        self.SendCommand(PCD_Command.CalcCrc)

        for i in range(0xFF):
            # The datasheet does not specify exact completion condition except
            # that FIFO buffer should contain 64 bytes.
            # While selftest is initiated by CalcCrc command
            # it behaves differently from normal CRC computation,
            # so one can't reliably use PCD_Register.DivIRq
            # to check for completion.
            # It is reported that some devices do not trigger CRCIRq flag
            # during selftest.
            n = self.ReadRegister(PCD_Register.FifoLevel)
            if n>=64:
                break
            time.sleep(0.05)

        self.UpdateRegister(PCD_Register.Command, PCD_Command.Idle)
        result=self.ReadRegister(PCD_Register.FifoData, 64)

        # deactivate auto-testing
        self.UpdateRegister(PCD_Register.AutoTest, 0x00)

        if ref_data is None:
            return False
        
        for i in len(ref_data):
            if ref_data[i]!=result[i]:
                # FIXME what is pgm_read_byte
                return False

        self.Init()
        return True

    # Power control functions

    def SoftPowerDown(self):
        """Power down the device by software.
            
        IMPORTANT NOTE:
        Calling any other function that uses PCD_Register.Command
        will disable soft power down mode !!!
        
        For more details about power control, refer to the datasheet, 
        section 8.6.
        """
        self.UpdateRegister(PCD_Register.Command, 1<<4, 1<<4)

    def SoftPowerUp(self):
        """Starts up the PCD.

        Raises:
            TimeoutError: If the device does not come up within 0.5s, 
            a timeout error is raised.
        """
        self.UpdateRegister(PCD_Register.Command, 0, 1<<4)
        deadline = time.time() + 0.5
        while time.time() < deadline:
            if 0!=self.ReadRegister(PCD_Register.Command, 1<<4):
                return
        raise TimeoutError()

    # Functions for communicating with PICCs
    def Transceive(
            self,
            data,
            rx_align = 0,
            tx_last_bits = 8,
            prefix_bytes = FifoBuffer(),
            check_crc = False
    ):
        recv = self.CommunicateWithPICC(PCD_Command.Transceive,
                                        (PCD_IrqBits.Idle, PCD_IrqBits.Rx),
                                        data,
                                        rx_align,
                                        tx_last_bits,
                                        prefix_bytes,
                                        True)
        if check_crc:
            self.CheckCrc(recv)
        return recv

    def CommunicateWithPICC(
            self,
            command,
            wait_irq,
            data,
            rx_align = 0,
            tx_last_bits = 0,
            prefix_bytes = FifoBuffer(),
            do_return_data = False
    ):
        """Communicate with a PICC.
        
        Parameters:
        command (PCD_Command): 
            A valid PCD Command, which is executed.
        wait_irq (int): 
            The bits in the PCD_Register.ComIRq that signal successful
            completion of the command.
        prefix_bytes (FifoBuffer): 
            Data, which will be prefixed to the result (taking rx_align into 
            account).
        rx_align (int): 
            An integer between [0,8), indicating the bit in the first byte
            that the received bytes should be aligned to. If this is >0 and
            data should be returned, then prefix_bytes must also be supplied
            and the last byte of prefixBytes should have rxAlign valid bits.
            In this case the last byte of prefixBytes will be updated from
            position rx_align onwards with the first received bits.
        tx_last_bits (int): 
            The number of valid bits in the last byte that is sent to the
            device. Must be in [1,8].
        do_return_data: 
            Whether or not to read and return the data from the FIFO buffer.

        Returns: 
        FifoBuffer: The received data prefixed by prefixBytes.
        """

        assert rx_align == prefix_bytes.valid_bits % 8, \
            "Unexpected: rx_align should be equal to prefix_bytes.valid_bits!"

        self.SendCommand(PCD_Command.Idle)
        self.ClearComIRqReg()
        self.FlushFifoBuffer()
        self.SendFifoData(data)
        self.SetBitFraming(rx_align, tx_last_bits)
        self.SendCommand(command)
        if command == PCD_Command.Transceive:
            self.StartTransceive()
        self.WaitForComIRqBit(wait_irq, 50) # 50ms timeout

        self.CheckForErrors()        
        self.CheckForErrors([PCD_Error.BufferOvfl,
                             PCD_Error.Parity,
                             PCD_Error.Protocol])

        if do_return_data:
            data = self.ReadFifoData(prefix_bytes=prefix_bytes)
        else:
            data = None

        return data

    def CheckCollisionOccured(self):
        """Checks whether or not a collision in the last command occured or not."""
        try:
            self.CheckForErrors(PCD_Error.Collision)
            return 0
        except CollisionError:
            return 1
    
    def CheckCrc(self, data):
        if len(data.data) == 1 and data.valid_bits == 4:
            raise RuntimeError("MIFARE NACK")
        if len(data.data) == 2 and data.valid_bits < 8:
            raise CrcError()
            
        crc = self.CalculateCrcBytes(data.data[:-2])
        if data.data[-2:] != crc:
            raise CrcError("The CRC is incorrect.")

    def CheckValidityOfCollisionPosition(self):
        collision_register = self.ReadRegister(PCD_Register.Coll)
        if collision_register & 0x20:
            raise RuntimeError("Collision position is not valid.")

    def GetCollisionPosition(self):
        self.CheckValidityOfCollisionPosition()
        position = self.ReadRegister(PCD_Register.Coll, 0x1F)
        if position == 0:
            position = 32
        return position
    
    
    def StopCrypto1(self):
        """Used to exit the PCD from its authenticated state.

        Remember to call this function after communicating
        with an authenticated PICC, otherwise no new communications can start.
        """
        self.ClearRegisterBitMask(PCD_Register.Status2, 0x08)

    # Support functions for debugging
    def DumpVersion(self):
        version_strings = {
            0x88: " = (clone)",
            0x90: " = v0.0",
            0x91: " = v1.0",
            0x92: " = v2.0",
            0x12: " = counterfeit chip"
        }
        v = self.ReadRegister(PCD_Register.Version)
        if v == 0 or v == 0xFF:
            logger.debug("WARNING: Communication failure")
        if v in version_strings:
            s = version_strings[v]
        else:
            s = " = unknown"
        logger.debug("Firmware Version: " + hex(v) + s)



def assertRegister(reg, varname=None):
    if varname is not None:
        err = "A PCD_Register is expected for " + varname + "."
    else:
        err = "A PCD_Register is expected as argument."
    assert type(reg)==PCD_Register, err
        
def maskRead(register):
    """Mask the address in register for reading.

    To indicate a read operation, the MSB must be set to 1.
    """
    return 0x80 | register

def maskWrite(register):
    """Mask the address in register for writing.

    To indicate a write operation, the MSB must be set to 0.
    """
    return (0xFF >> 1) & register

