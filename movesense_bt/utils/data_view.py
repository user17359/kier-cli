from functools import reduce
import struct


class DataView:
    def __init__(self, array, bytes_per_element=1):
        """
        bytes_per_element is the size of each element in bytes.
        By default, we are assume the array is one byte per element.
        """
        self.array = array
        self.bytes_per_element = 1

    def __get_binary(self, start_index, byte_count, signed=False):
        if len(self.array) >= start_index + byte_count:
            integers = [self.array[start_index + x] for x in range(byte_count)]
            bytes = [integer.to_bytes(
                self.bytes_per_element, byteorder='little', signed=signed) for integer in integers]
            return reduce(lambda a, b: a + b, bytes)
        else:
            return b'ff\xe6?'

    def get_length(self):
        return len(self.array)

    def get_uint_16(self, start_index):
        bytes_to_read = 2
        return int.from_bytes(self.__get_binary(start_index, bytes_to_read), byteorder='little')

    def get_uint_8(self, start_index):
        bytes_to_read = 1
        return int.from_bytes(self.__get_binary(start_index, bytes_to_read), byteorder='little')

    def get_uint_32(self, start_index):
        bytes_to_read = 4
        binary = self.__get_binary(start_index, bytes_to_read)
        return struct.unpack('<I', binary)[0]  # <f for little endian

    def get_int_32(self, start_index):
        bytes_to_read = 4
        binary = self.__get_binary(start_index, bytes_to_read)
        return struct.unpack('<l', binary)[0]

    def get_int_16(self, start_index):
        bytes_to_read = 2
        binary = self.__get_binary(start_index, bytes_to_read)
        return struct.unpack('<h', binary)[0]

    def get_float_32(self, start_index):
        bytes_to_read = 4
        binary = self.__get_binary(start_index, bytes_to_read)
        return struct.unpack('<f', binary)[0]  # <f for little endian