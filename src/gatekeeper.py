import subprocess
import json
import requests
import time
import ConfigParser
import hashlib

# Load configs
config = ConfigParser.ConfigParser()
config.read("gatekeeper.cfg")

host = config.get('Server', 'host')
port = config.get('Server', 'port')

secret_key = config.get('Crypto', 'secret_key')

hikaruspace_address = 'http://' + host + ':' + port

print "Gatekeeper, ENGAGED!"
print "===================="

# Scan forever and ever and ever and ever
while True:
    # Grab the output from poll.py
    results = subprocess.check_output(['/usr/bin/sudo','/usr/bin/python3',
'/home/pi/hikaru-gatekeeper/src/poll.py'])
    print "Card scanned!"
    print results
    # Store the timestamp to then use it to hash
    timestamp = time.time()
    print "Timestamp: " + str(timestamp)

    # Convert the JSON into a list, then send it to Hikaruspace
    scan_results = json.loads(results)
    try:
        r = requests.get(hikaruspace_address + '/validate_card',
        params={'reader_id':scan_results['reader_id'], 
                'card_uid':scan_results['card_uid'],
                'status':scan_results['status'],
                'timestamp':timestamp})
        card_uid = scan_results['card_uid']

        print "Triggering " + r.url
        print "Response: " + r.text
        
        # Hash+salt the timestamp
        hashed_time = hashlib.sha224()
        hashed_time.update(secret_key + str(timestamp))
        print "Hashed time: " + hashed_time.hexdigest()

    except requests.ConnectionError:
        print "Could not reach " + hikaruspace_address
        print "CONNECTION ERROR: Either Hikaruspace is down, your connection is down, or the configs are off."

        

    # Cleanup for next scan, just in case there could be residual something
    timestamp = 0
    card_uid = 0

    
