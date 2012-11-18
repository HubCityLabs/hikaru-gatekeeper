"""This module represents a communication frame for the PN532 NFC Chip.

@author:  DanyO <me@danyo.ca>
@license: The source code within this file is licensed under the BSD 2 Clause license.
          See LICENSE file for more information.

"""

import os
import sys
lib_path = os.path.abspath('../lib')
sys.path.append(lib_path)

from pyPN532.i2c import *
from pyPN532.frame import *
from pyPN532.constants import *


class Pn532Frame:
    def __init__(
        self, frame_type=PN532_FRAME_TYPE_DATA,
        preamble=0x00,
        startCode1=0x00,
        startCode2=0xFF,
        frameIdentifier=0xD4,
        data=bytearray(),
            postamble=0x00):

        self._frame_type = frame_type
        self._preamble = preamble
        self._startCode1 = startCode1
        self._startCode2 = startCode2
        self._frameIdentifier = frameIdentifier
        self._data = data
        self._postamble = postamble

    def get_length(self):
        return len(self._data) + 1

    def get_length_checksum(self):
        return (~self.get_length() & 0xFF) + 0x01

    def get_data(self):
        return self._data

    def get_data_checksum(self):
        byteArray = bytearray()

        for byte in self._data:
            byteArray.append(byte)

        byteArray.append(self._frameIdentifier)

        inverse = (~sum(byteArray) & 0xFF) + 0x01

        if inverse > 255:
            inverse = inverse - 255

        return inverse

    def get_frame_type(self):
        return self._frame_type

    def to_tuple(self):
        byteArray = bytearray()

        if self._frame_type == PN532_FRAME_TYPE_ACK:
            byteArray.append(PN532_PREAMBLE)
            byteArray.append(PN532_START_CODE_1)
            byteArray.append(PN532_START_CODE_2)
            byteArray.append(PN532_START_CODE_1)
            byteArray.append(PN532_START_CODE_2)
            byteArray.append(PN532_POSTAMBLE)

            return (byteArray)

        byteArray.append(self._preamble)
        byteArray.append(self._startCode1)
        byteArray.append(self._startCode2)
        byteArray.append(self.get_length())
        byteArray.append(self.get_length_checksum())
        byteArray.append(self._frameIdentifier)

        for byte in self._data:
            byteArray.append(byte)

        byteArray.append(self.get_data_checksum())
        byteArray.append(self._postamble)

        return (byteArray)

    @staticmethod
    def from_response(response):
        if Pn532Frame.is_valid_response(response) is not True:
            raise RuntimeError("Invalid Response")

        if Pn532Frame.is_ack(response):
            return Pn532Frame(frame_type=PN532_FRAME_TYPE_ACK,
                              frameIdentifier=0x00)

        response_length = response[0][PN532_FRAME_POSITION_LENGTH] + 1
        data = bytearray(
            response[0][PN532_FRAME_POSITION_DATA_START:PN532_FRAME_POSITION_DATA_START + response_length - 2])

        return Pn532Frame(
            preamble=response[0][PN532_FRAME_POSITION_PREAMBLE],
            startCode1=response[0][PN532_FRAME_POSITION_START_CODE_1],
            startCode2=response[0][PN532_FRAME_POSITION_START_CODE_2],
            frameIdentifier=response[0][
                PN532_FRAME_POSITION_FRAME_IDENTIFIER],
            data=data,
            postamble=response[0][PN532_FRAME_POSITION_DATA_START + response_length + 2])

    @staticmethod
    def is_valid_response(response):
        if (response[0][0] & 0x01) == 0x01:
            if response[0][PN532_FRAME_POSITION_PREAMBLE] == PN532_PREAMBLE:
                if response[0][PN532_FRAME_POSITION_START_CODE_1] == PN532_START_CODE_1:
                    if response[0][PN532_FRAME_POSITION_START_CODE_2] == PN532_START_CODE_2:
                        return True

        return False

    @staticmethod
    def is_ack(response):
        if response[0][PN532_FRAME_POSITION_LENGTH] == 0x00:
            if response[0][PN532_FRAME_POSITION_LENGTH_CHECKSUM] == 0xFF:
                if response[0][PN532_FRAME_POSITION_FRAME_IDENTIFIER] == 0x00:
                    return True

        return False
