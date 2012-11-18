#from libPN532_i2c_RPi import Pn532_i2c
#import hashlib


class nfc_poller:

    def __init__(self):
        self._address = 0x24
        #self._pn532 = Pn532_i2c(0x24, 1)
        #self._pn532.SAMconfigure()

    def create_json_response(self, reader_id, card_uid, status):
        json = """{"reader_id":"<reader_id>","card_uid":"<card_uid>","status":"<status>"}"""
        json = json.replace("<reader_id>", str(reader_id))
        json = json.replace("<card_uid>", card_uid)
        json = json.replace("<status>", status)

        return json

    def poll(self):
        #card_uid = self._pn532.read_mifare().get_data()

        json = self.create_json_response(self._address, "093254afe4bc3ff22cf54e507b57fa2965b9215960efc6ecd28573f3a96f637ac89e48c1b3d7a7c48796c01061f3487937780aedfc5016aaf09bcdaef3e93b0b", "OK")
        return json

    def __exit__(self, type, value, traceback):
        del self._pn532
