#!/usr/bin/env python3
import os
import sys
lib_path = os.path.abspath('../lib')
sys.path.append(lib_path)

from nfc_poller import *

test = nfc_poller()
print(test.poll())
