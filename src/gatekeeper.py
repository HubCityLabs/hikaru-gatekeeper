import subprocess
import json
import requests

# Scan forever and ever and ever and ever
while True:
    # Grab the output from poll.py
    results = subprocess.check_output(['/usr/bin/sudo','/usr/bin/python3',
'/home/pi/hikaru-gatekeeper/src/poll.py'])
    print "Card scanned!"
    print results

    # Convert the JSON into a list, then send it to Hikaruspace
    scan_results = json.loads(results)
    r = requests.get('http://moncton.zombievolk.com:9999/update_clients',
            params={'reader_id':scan_results['reader_id'], 
                    'card_uid':scan_results['card_uid'],
                    'status':scan_results['status']})
    print "Triggering " + r.url
