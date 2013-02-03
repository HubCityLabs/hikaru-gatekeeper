#!/usr/bin/env python3
import os
import sys

lib_path = os.path.abspath('../lib')
sys.path.append(lib_path)

from nfc_poller import *

# Listen to infinity!
while True:
    try:
        poller = nfc_poller()
        results = poller.poll()
        print(results)
        exit(0)
    except KeyboardInterrupt:
        s.close()
        exit(0)
        
