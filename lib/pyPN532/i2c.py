"""This module takes care of I2C communication between the host and PN532 NFC Chip.

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
from quick2wire.i2c import I2CMaster, reading, writing
from time import sleep
import logging

LOGGING_ENABLED = False
LOG_LEVEL = logging.DEBUG
DEFAULT_DELAY = 0.005


class Pn532_i2c:
    PN532 = None
    address = None
    i2cChannel = None
    logger = None

    def __init__(self, address, i2cChannel):
        self.logger = logging.getLogger()
        self.logger.propagate = LOGGING_ENABLED
        if self.logger.propagate:
            self.logger.setLevel("DEBUG")

        self.address = address
        self.i2cChannel = i2cChannel
        self.PN532 = I2CMaster(self.i2cChannel)

    def send_command_check_ack(self, frame):
        self.send_command(frame)
        if self.read_ack():
            return True
        else:
            return False

    def read_response(self):
        logging.debug("readResponse...")
        response = [b'\x00\x00\x00\x00\x00\x00\x00']

        while True:

            try:
                logging.debug("readResponse..............Reading.")

                sleep(DEFAULT_DELAY)
                response = self.PN532.transaction(
                    reading(self.address, 255))
                logging.debug(response)
                logging.debug("readResponse..............Read.")
            except Exception:
                pass
            else:
                try:
                    frame = Pn532Frame.from_response(response)

                    # Acknowledge Data frames coming from the PN532
                    if frame.get_frame_type() == PN532_FRAME_TYPE_DATA:
                        self.send_command(Pn532Frame(
                            frame_type=PN532_FRAME_TYPE_ACK))

                except Exception as ex:
                    logging.debug(ex)
                    logging.debug(ex.args)
                    pass
                else:
                    return frame

    def send_command(self, frame):
        logging.debug("send_command...")

        while True:
            try:
                logging.debug("send_command...........Sending.")

                sleep(DEFAULT_DELAY)
                self.PN532.transaction(
                    writing(self.address, frame.to_tuple()))

                logging.debug("send_command...........Sent.")
            except Exception as ex:
                logging.debug(ex)

                self.reset_i2c()
                sleep(DEFAULT_DELAY)
            else:
                return True

    def read_ack(self):
        logging.debug("read_ack...")

        while True:
            sleep(DEFAULT_DELAY)
            response_frame = self.read_response()

            if response_frame.get_frame_type() == PN532_FRAME_TYPE_ACK:
                return True
            else:
                pass

    def read_mifare(self):
        frame = Pn532Frame(frame_type=PN532_FRAME_TYPE_DATA, data=bytearray([PN532_COMMAND_INLISTPASSIVETARGET, 0x01, 0x00]))
        self.send_command_check_ack(frame)

        return self.read_response()

    def reset_i2c(self):
        logging.debug("I2C Reset...")

        self.PN532.close()
        del self.PN532
        self.PN532 = I2CMaster(self.i2cChannel)

        logging.debug("I2C Reset............Created.")

    def SAMconfigure(self):
        frame = Pn532Frame(frame_type=PN532_FRAME_TYPE_DATA, data=bytearray([PN532_COMMAND_SAMCONFIGURATION, PN532_SAMCONFIGURATION_MODE_NORMAL, 0x01, 0x00]))
        self.send_command_check_ack(frame)

    def __exit__(self, type, value, traceback):
        self.PN532.close()
        del self.PN532
