import os
import sys
lib_path = os.path.abspath('../lib')
sys.path.append(lib_path)

from pyPN532.i2c import *
from pyPN532.frame import *
from pyPN532.constants import *

import hashlib


class nfc_poller:

    def __init__(self):
        self._address = 0x24
        self._pn532 = Pn532_i2c(0x24, 1)
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
