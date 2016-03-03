import logging
import re
import smbus

__author__ = "Fernando Chorney <fchorney@djsbx.com>"
__version__ = "1.0.0"

log = logging.getLogger(__name__)


class I2C(object):
    def __init__(self, address, bus=None):
        log.debug("Initializing I2C bus for address: 0x%02X" % address)
        self.address = address
        self.bus = None

        # Connect to the I2C bus
        self.__connect_to_bus(bus)

        # Test the connection to make sure we're connected to the right address
        try:
            test = self.read_raw_byte()
        except IOError as e:
            log.error(
                "I2C Test Connection Failed for Address: 0x%02X" % self.address
            )
            raise

        log.debug("Successfully Connected to 0x%02X" % address)

    def clean_up(self):
        """
        Close the I2C bus
        """
        log.debug("Closing I2C bus for address: 0x%02X" % self.address)
        self.bus.close()

    # Write Functions

    def write_quick(self):
        """
        Send only the read / write bit
        """
        self.bus.write_quick(self.address)
        log.debug("write_quick: Sent the read / write bit")

    def write_byte(self, cmd, value):
        """
        Writes an 8-bit byte to the specified command register
        """
        self.bus.write_byte_data(self.address, cmd, value)
        log.debug(
            "write_byte: Wrote 0x%02X to command register 0x%02X" % (
                value, cmd
            )
        )

    def write_word(self, cmd, value):
        """
        Writes a 16-bit word to the specified command register
        """
        self.bus.write_word_data(self.address, cmd, value)
        log.debug(
            "write_word: Wrote 0x%04X to command register 0x%02X" % (
                value, cmd
            )
        )

    def write_raw_byte(self, value):
        """
        Writes an 8-bit byte directly to the bus
        """
        self.bus.write_byte(self.address, value)
        log.debug("write_raw_byte: Wrote 0x%02X" % value)

    def write_block_data(self, cmd, block):
        """
        Writes a block of bytes to the bus using I2C format to the specified
        command register
        """
        self.bus.write_i2c_block_data(self.address, cmd, block)
        log.debug(
            "write_block_data: Wrote [%s] to command register 0x%02X" % (
                ', '.join(['0x%02x' % x for x in block]),
                cmd
            )
        )

    # Read Functions

    def read_raw_byte(self):
        """
        Read an 8-bit byte directly from the bus
        """
        result = self.bus.read_byte(self.address)
        log.debug("read_raw_byte: Read 0x%02X from the bus" % result)
        return result

    def read_block_data(self, cmd, length):
        """
        Read a block of bytes from the bus from the specified command register
        Amount of bytes read in is defined by length
        """
        results = self.bus.read_i2c_block_data(self.address, cmd, length)
        log.debug(
            "read_block_data: Read [%s] from command register 0x%02X" % (
                ', '.join(['0x%02X' % x for x in results]),
                cmd
            )
        )
        return results

    def read_unsigned_byte(self, cmd):
        """
        Read an unsigned byte from the specified command register
        """
        result = self.bus.read_byte_data(self.address, cmd)
        log.debug(
            "read_unsigned_byte: Read 0x%02x from command register 0x%02x" % (
                result, cmd
            )
        )
        return result

    def read_signed_byte(self, cmd):
        """
        Read a signed byte from the specified command register
        """
        result = self.bus.read_byte_data(self.address, cmd)

        # Convert to signed data
        if result > 127:
            result -= 256

        log.debug(
            "read_signed_byte: Read 0x%02x from command register 0x%02X" % (
                result, cmd
            )
        )
        return result

    def read_unsigned_word(self, cmd, little_endian=True):
        """
        Read an unsigned word from the specified command register
        We assume the data is in little endian mode, if it is in big endian
        mode then set little_endian to False
        """
        result = self.bus.read_word_data(self.address, cmd)

        if not little_endian:
            result = ((result << 8) & 0xFF00) + (result >> 8)

        log.debug(
            "read_unsigned_word: Read 0x%04X from command register 0x%02X" % (
                result, cmd
            )
        )
        return result

    def read_signed_word(self, cmd, little_endian=True):
        """
        Read a signed word from the specified command register
        We assume the data is in little endian mode, if it is in big endian
        mode then set little_endian to False
        """
        result = self.bus.read_word_data(self.address, cmd)

        if not little_endian:
            result = ((result << 8) & 0xFF00) + (result >> 8)

        # Convert to signed data
        if result > 32767:
            result -= 65536

        log.debug(
            "read_signed_word: Read 0x%04X from command register 0x%02X" % (
                result, cmd
            )
        )
        return result

    def __connect_to_bus(self, bus):
        """
        Attempt to connect to an I2C bus
        """
        def connect(bus_num):
            try:
                log.debug("Attempting to connect to bus %s..." % bus_num)
                self.bus = smbus.SMBus(bus_num)
                log.debug("Success")
            except IOError as e:
                log.debug("Failed")
                raise

        # If the bus is not explicitly stated, try 0 and then try 1 if that
        # fails
        if bus is None:
            try:
                connect(0)
                return
            except IOError as e:
                pass

            try:
                connect(1)
                return
            except IOError as e:
                raise
        else:
            try:
                connect(bus)
                return
            except IOError as e:
                raise
