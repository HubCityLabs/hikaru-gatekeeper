#!/usr/bin/env python3
import os
import sys
import socket

lib_path = os.path.abspath('../lib')
sys.path.append(lib_path)

from nfc_poller import *

# Configs
host = '192.168.2.46'
port = 50000
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

# Listen to infinity!
while True:
    try:
        poller = nfc_poller()
        results = poller.poll()
        print(results)
        byte_results = bytes(results, 'UTF-8')
        
        try:
            s.send(byte_results)
            data = s.recv(size)
        except socket.error:
            print("Broken pipe! Reconnecting...")
            s.close()
            s.connect((host,port))
            print("And here?")
            s.send(byte_results)
            data = s.recv(size)
            
        print('Received:', data)
    except KeyboardInterrupt:
        s.close()
        print('Bye now!')
        sys.exit(0)
        
