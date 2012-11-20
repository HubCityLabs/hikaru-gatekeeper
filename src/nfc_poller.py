import os
import sys
lib_path = os.path.abspath('../lib')
sys.path.append(lib_path)

from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *

import hashlib


class nfc_poller:

    def __init__(self):
        self._address = RPI_DEFAULT_I2C_NEW
        self._pn532 = Pn532_i2c()
        self._pn532.SAMconfigure()

    def create_json_response(self, reader_id, card_uid, status):
        json = """{"reader_id":"<reader_id>","card_uid":"<card_uid>","status":"<status>"}"""
        json = json.replace("<reader_id>", str(reader_id))
        json = json.replace("<card_uid>", card_uid)
        json = json.replace("<status>", status)

        return json

    def poll(self):
        card_uid = self._pn532.read_mifare().get_data()

        json = self.create_json_response(
            self._address, hashlib.sha512(card_uid).hexdigest(), "OK")
        return json

    def __exit__(self, type, value, traceback):
        del self._pn532
